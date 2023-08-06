"""Filtering functionality"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import Optional
from typing import Union

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from tensorflow import linalg as tfl
from tensorflow.types.experimental import TensorLike
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import prefer_static as ps

from dyno import distributions
from dyno import linalg


@dataclass
class Options:
    """Options to control the details of filtering"""

    approximate_log_likelihood_with_predicted_mean: bool = False
    log_likelihood_fn: distributions.ProbFunction = distributions.ProbFunction.LOG_PROB
    assert_convergence: bool = True
    use_bfgs_inverse_hessian_estimate: bool = True
    trace: bool = False
    predict_qoi: bool = False
    burnin_timesteps: int = 0
    final_step_only: bool = False
    bfgs_args: dict = field(default_factory=dict)
    initial_inverse_hessian_scale: Optional[float] = None

    # If True, we use a manual (rather hacky) implementation
    # of `tfp.math.value_and_gradient`, involving a call to
    # `tf.gradients(..., gate_gradients=True)`.
    #
    # This gate_gradients argument is something to do with
    # ensuring reproducibility (so gradients are applied in
    # the correct order, or something), and we are hoping
    # that by using it we will get a stable model.
    #
    # `tfp.math.value_and_gradient` calls `tf.gradients`
    # already under the hood, but doesn't allow the passing
    # through of the `gate_gradients` argument, annoyingly.
    # That's why we've had to do a "manual" implementation.
    alternative_value_and_gradient_fn: bool = False

    # A unique per-instance identifier for saving
    # fit results.
    # We could adjust this to contain details such
    # as the branch name - but for now dyno has no
    # knowledge of such things. Hopefully this is
    # sufficient to be useful.
    uuid: str = field(default_factory=lambda: str(uuid.uuid4())[0:10])


def _build_kalman_has_observations_true_fn(
    prior_mean, prior_cov, observation_matrix, observation_noise, observation
):
    """Function for the observations case in the Kalman filter"""

    # put all logic inside function so it may be conditionally executed

    def has_observations_true():
        # Given predicted mean u_{t|t-1} and covariance P_{t|t-1} from the previous
        # step, incorporate the observation, producing the filtered mean u_t and
        # covariance P_t.
        filtered_mean, filtered_cov, observation_dist = _linear_gaussian_update(
            prior_mean, prior_cov, observation_matrix, observation_noise, observation
        )

        # Compute the marginal likelihood p(x_t | x_{:t-1}) for this observation.
        log_marginal_likelihood = observation_dist.log_prob(observation)

        return log_marginal_likelihood, filtered_mean, filtered_cov

    return has_observations_true


def _build_has_observations_false_fn(prior_mean, prior_cov, batch_shape):
    """Function for filtered output in the case of no observations"""

    # put all logic inside function so it may be conditionally executed

    def has_observations_false():
        filtered_mean = prior_mean
        filtered_cov = prior_cov
        dtype = dtype_util.common_dtype([prior_mean, prior_cov])
        log_marginal_likelihood = tf.zeros(batch_shape, dtype=dtype)

        return log_marginal_likelihood, filtered_mean, filtered_cov

    return has_observations_false


def _propagate_mean(mean, linop, dist):
    """Propagate a mean through linear Gaussian transformation."""

    return linop.matvec(mean) + dist.mean()


def _propagate_cov(cov, linop, dist):
    """Propagate covariance through linear Gaussian transformation."""

    # For linop A and input cov P, returns `A P A' + dist.cov()`
    return linop.matmul(linop.matmul(cov), adjoint_arg=True) + dist.covariance()


def _kalman_transition(
    filtered_mean, filtered_cov, transition_matrix, transition_noise
):
    """Propagate a filtered distribution through a transition model."""

    # Run the filtered posterior through the transition model to predict the next time
    # step:
    #  u_{t|t-1} = F_t u_{t-1} + b_t
    #  P_{t|t-1} = F_t P_{t-1} F_t' + Q_t
    predicted_mean = _propagate_mean(filtered_mean, transition_matrix, transition_noise)
    predicted_cov = _propagate_cov(filtered_cov, transition_matrix, transition_noise)

    return predicted_mean, predicted_cov


def _linear_gaussian_update(
    prior_mean, prior_cov, observation_matrix, observation_noise, observation
):
    """Conjugate update for a linear Gaussian model"""

    # Push the predicted mean for the latent state through the observation model
    obs_expected = _propagate_mean(prior_mean, observation_matrix, observation_noise)

    # Push the predictive covariance of the latent state through the observation model:
    #  S = R + H * P * H'.
    # We use a temporary variable for H * P, reused below to compute Kalman gain.
    tmp_obs_cov = observation_matrix.matmul(prior_cov)
    predicted_obs_cov = (
        observation_matrix.matmul(tmp_obs_cov, adjoint_arg=True)
        + observation_noise.covariance()
    )

    # Compute optimal Kalman gain:
    #  K = P * H' * S^{-1}
    # Since both S and P are cov matrices, thus symmetric, we can take the transpose and
    # reuse our previous computation:
    #      = (S^{-1} * H * P)'
    #      = (S^{-1} * tmp_obs_cov) '
    #      = (S \ tmp_obs_cov)'
    predicted_obs_cov_chol = tfl.cholesky(predicted_obs_cov)
    gain_transpose = tfl.cholesky_solve(predicted_obs_cov_chol, tmp_obs_cov)

    # Compute the posterior mean, incorporating the observation.
    #  u* = u + K (observation - obs_expected)
    posterior_mean = prior_mean + tfl.matvec(
        gain_transpose, observation - obs_expected, adjoint_a=True
    )

    # For the posterior covariance, we could use the simple update
    #  P* = P - K * H * P
    # but this is prone to numerical issues because it subtracts a value from a PSD
    # matrix.  We choose instead to use the more expensive Jordan form update
    #  P* = (I - K H) * P * (I - K H)' + K R K'
    # which always produces a PSD result. This uses
    #  tmp_term = (I - K * H)'
    # as an intermediate quantity.
    tmp_term = -observation_matrix.matmul(gain_transpose, adjoint=True)  # -K * H
    tmp_term = tfl.set_diag(tmp_term, tfl.diag_part(tmp_term) + 1)
    posterior_cov = tfl.matmul(
        tmp_term, tfl.matmul(prior_cov, tmp_term), adjoint_a=True
    ) + tfl.matmul(
        gain_transpose,
        tfl.matmul(observation_noise.covariance(), gain_transpose),
        adjoint_a=True,
    )

    predictive_dist = tfd.MultivariateNormalTriL(
        loc=obs_expected, scale_tril=predicted_obs_cov_chol
    )

    return posterior_mean, posterior_cov, predictive_dist


def _build_neg_log_prob_fn(prior_dist, observation_dist_fn, observation):
    """Objective function for the Laplace approximation"""

    def neg_log_prob_fn(latent_state):

        prior_log_prob = prior_dist.log_prob(latent_state)
        observation_dist = observation_dist_fn(latent_state)
        observation_log_prob = observation_dist.log_prob(observation)

        return -(prior_log_prob + observation_log_prob)

    return neg_log_prob_fn


def _build_laplace_gaussian_has_observations_true_fn(
    observation_dist_fn, observation, prior_mean, prior_cov, batch_shape, options
):
    """Function for the observations case in the Laplace Gaussian filter"""

    def has_observations_true():

        latent_size = prior_mean.shape[-1]

        prior_dist = tfd.MultivariateNormalTriL(
            loc=prior_mean, scale_tril=tfl.cholesky(prior_cov)
        )

        neg_log_prob_fn = _build_neg_log_prob_fn(
            prior_dist=prior_dist,
            observation_dist_fn=observation_dist_fn,
            observation=observation,
        )

        initial_position = tf.broadcast_to(
            prior_mean, tf.concat([batch_shape, [latent_size]], axis=0)
        )

        if options.initial_inverse_hessian_scale is None:
            initial_inverse_hessian_estimate = prior_cov
        else:
            initial_inverse_hessian_estimate = (
                prior_cov * options.initial_inverse_hessian_scale
            )

        bfgs_args = options.bfgs_args.copy()
        parallel_iterations = bfgs_args.pop("parallel_iterations", 10)
        max_iterations = bfgs_args.pop("max_iterations", 1_000)
        max_line_search_iterations = bfgs_args.pop("max_line_search_iterations", 1_000)

        def value_and_grad_fn(x):
            if options.alternative_value_and_gradient_fn:
                # NOTE: This approach only works when wrapping with
                #       `@tf.function`. It can't be used in eager mode.
                value = neg_log_prob_fn(x)
                grad = tf.gradients(value, x, gate_gradients=True)[0]
            else:
                value, grad = tfp.math.value_and_gradient(neg_log_prob_fn, x)
            return value, grad

        optim = tfp.optimizer.bfgs_minimize(
            value_and_grad_fn,
            initial_position=initial_position,
            initial_inverse_hessian_estimate=initial_inverse_hessian_estimate,
            validate_args=False,
            parallel_iterations=parallel_iterations,
            max_iterations=max_iterations,
            max_line_search_iterations=max_line_search_iterations,
            **bfgs_args,
        )

        if options.assert_convergence:
            converged = optim.converged
            not_failed = tf.logical_not(optim.failed)
            condition = tf.reduce_all(converged) & tf.reduce_all(not_failed)
            assertions = [
                tf.debugging.Assert(
                    condition=condition, data=optim, name="bfgs_convergence"
                )
            ]
        else:
            assertions = []

        with tf.control_dependencies(assertions):
            solution = optim.position

        if options.use_bfgs_inverse_hessian_estimate:
            inv_hessian = optim.inverse_hessian_estimate
        else:
            _, hessian = linalg.value_and_hessian(neg_log_prob_fn, solution)
            inv_hessian = linalg.symmetric_inv(hessian)

        if options.approximate_log_likelihood_with_predicted_mean:
            # TODO(jeff): unit tests for this case
            observation_dist = observation_dist_fn(prior_mean)
            log_prob_fn = getattr(observation_dist, options.log_likelihood_fn.value)
            log_marginal_likelihood = log_prob_fn(observation)
        else:
            if options.log_likelihood_fn != distributions.ProbFunction.LOG_PROB:
                error_msg = (
                    "Laplace approximation for the marginal likelihood only "
                    "supports 'LOG_PROB' log_likelihood_fn currently"
                )
                raise NotImplementedError(error_msg)

            half_log_two_pi = tf.constant(0.5 * np.log(2 * np.pi), dtype=solution.dtype)

            log_marginal_likelihood = (
                -optim.objective_value
                + latent_size * half_log_two_pi
                + 0.5 * tfl.logdet(inv_hessian)
            )

        filtered_mean = solution
        filtered_cov = inv_hessian

        return log_marginal_likelihood, filtered_mean, filtered_cov

    return has_observations_true


def kalman_filter_step(
    observation: TensorLike,
    transition_matrix: tfl.LinearOperator,
    transition_noise: tfd.Distribution,
    observation_matrix: tfl.LinearOperator,
    observation_noise: tfd.Distribution,
    prior_mean: TensorLike,
    prior_cov: TensorLike,
    batch_shape: tf.TensorShape = tf.TensorShape([]),
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Perform one step of the KF algorithm.

    This is an algorithm for estimation of the latent state for linear Gaussian state
    space models. Since everything is linear (the relationship between the latent state
    and the observations + the transition model) and the observations + initial state
    prior is Gaussian, the latent state is Gaussian at every time step and there are no
    approximations involved.

    Returns:

    log_marginal_likelihood: p(obs[:t+1] | obs[:t]).

    predicted_{mean/cov}: The latent state distribution statistics for the next step,
        that is, p(latent[t+1] | y[:t]) where this function is exactly the Gaussin
        density function.

    filtered_{mean/cov}: The latent state distribution statistics at the end of this
        step, that is, p(latent[t] | y[:t]) under a Gaussian assumption for the
        distribution of latent.

    """

    has_observations_true = _build_kalman_has_observations_true_fn(
        prior_mean, prior_cov, observation_matrix, observation_noise, observation
    )

    has_observations_false = _build_has_observations_false_fn(
        prior_mean, prior_cov, batch_shape
    )

    log_marginal_likelihood, filtered_mean, filtered_cov = tf.cond(
        ps.shape(observation)[0] > 0, has_observations_true, has_observations_false
    )

    predicted_mean, predicted_cov = _kalman_transition(
        filtered_mean, filtered_cov, transition_matrix, transition_noise
    )

    return (
        log_marginal_likelihood,
        predicted_mean,
        predicted_cov,
        filtered_mean,
        filtered_cov,
    )


def laplace_gaussian_step(
    observation_dist_fn: Callable,
    observation: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
    transition_matrix: tfl.LinearOperator,
    transition_noise: tfd.Distribution,
    prior_mean: TensorLike,
    prior_cov: TensorLike,
    batch_shape: tf.TensorShape = tf.TensorShape([]),
    options: Options = Options(),
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Perform one step of the LGF algorithm.

    This approximates the latent state with a Gaussian distribution, and is suitable for
    general (i.e. non Gaussian) observations.

    Returns:

    log_marginal_likelihood: An estimate of p(obs[:t+1] | obs[:t]).

    predicted_{mean/cov}: The latent state distribution statistics for the next step,
        that is, p(latent[t+1] | y[:t]) under a Gaussian assumption for the distribution
        of latent.

    filtered_{mean/cov}: The latent state distribution statistics at the end of this
        step, that is, p(latent[t] | y[:t]) under a Gaussian assumption for the
        distribution of latent.

    """

    if isinstance(observation, (tuple, list)):
        has_observations = tf.reduce_any([ps.shape(x)[0] > 0 for x in observation])
    else:
        has_observations = ps.shape(observation)[0] > 0

    has_observations_true = _build_laplace_gaussian_has_observations_true_fn(
        observation_dist_fn=observation_dist_fn,
        observation=observation,
        prior_mean=prior_mean,
        prior_cov=prior_cov,
        batch_shape=batch_shape,
        options=options,
    )

    has_observations_false = _build_has_observations_false_fn(
        prior_mean, prior_cov, batch_shape
    )

    log_marginal_likelihood, filtered_mean, filtered_cov = tf.cond(
        has_observations, has_observations_true, has_observations_false
    )

    predicted_mean, predicted_cov = _kalman_transition(
        filtered_mean, filtered_cov, transition_matrix, transition_noise
    )

    return (
        log_marginal_likelihood,
        predicted_mean,
        predicted_cov,
        filtered_mean,
        filtered_cov,
    )
