"""State space models"""

import functools
import warnings

from dataclasses import make_dataclass
from typing import Any
from typing import Callable
from typing import NamedTuple
from typing import Optional
from typing import Union

import tensorflow as tf

from tensorflow import linalg as tfl
from tensorflow.types.experimental import TensorLike
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import distribution_util
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import prefer_static as ps

from dyno import filtering
from dyno import structural_time_series as sts
from dyno import util


class ForwardFilterResults(NamedTuple):
    final_step_predicted_mean: tf.Tensor
    final_step_predicted_cov: tf.Tensor
    log_likelihoods: Optional[tf.Tensor] = None
    cumulative_log_likelihood: Optional[tf.Tensor] = None
    predicted_means: Optional[tf.Tensor] = None
    predicted_cov_diags: Optional[tf.Tensor] = None
    predicted_qois: Optional[tf.Tensor] = None


class AdditiveSSM:
    """State space model comprised of components"""

    def __init__(
        self,
        components: list[sts.Component],
        initial_batch_shape: tf.TensorShape = tf.TensorShape([]),
    ):

        latent_sizes = [x.latent_size for x in components]

        self._latent_size = sum(latent_sizes)
        self._components = components
        self._dtype = dtype_util.common_dtype(components)

        self._initial_state_prior = util.factored_joint_mvn(
            [x.initial_state_prior for x in components]
        )

        self._batch_shape = functools.reduce(
            tf.broadcast_static_shape,
            [initial_batch_shape] + [x.batch_shape for x in components],
        )

    def forward_filter_step(
        self,
        observation: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
        prior_mean: TensorLike,
        prior_cov: TensorLike,
        filter_options: filtering.Options,
        **step_covariates,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        """Run filtering for one timestep"""

        raise NotImplementedError("`forward_filter_step` has not been overriden")

    def predict_step(
        self, predicted_mean: TensorLike, predicted_cov: TensorLike, **step_covariates
    ) -> tfd.Distribution:
        """Prediction for a single step"""

        raise NotImplementedError("`predict_step` has not been overriden")

    def predict_qoi(
        self, predicted_mean: TensorLike, predicted_cov: TensorLike, **step_covariates
    ) -> Any:
        """predict the 'quantity of interest'"""

        raise NotImplementedError("`predict_qoi` has not been overriden")

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        """Transition matrix for a single step"""

        return tfl.LinearOperatorBlockDiag(
            [x.transition_matrix(**step_covariates) for x in self._components]
        )

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        """Transition noise for a single step"""

        return util.factored_joint_mvn(
            [x.transition_noise(**step_covariates) for x in self._components]
        )

    def observation_matrix(self, **step_covariates) -> tfl.LinearOperator:
        """Observation matrix for a single step"""

        components = [x.observation_matrix(**step_covariates) for x in self._components]

        return tfl.LinearOperatorFullMatrix(tf.concat(components, axis=-1))

    def _decomposed_latent_state_cls(self):
        return make_dataclass(
            "DecomposedLatentState", [(x, tf.Tensor) for x in self.component_names]
        )

    def _step_observation(self, observations, timestep):
        if isinstance(observations, (tuple, list)):
            return [x[timestep] for x in observations]
        return observations[timestep]

    def _step_covariates(self, covariates, timestep):
        return {k: v[timestep] for k, v in covariates.items()}

    def _num_timesteps(self, observations):
        if isinstance(observations, (tuple, list)):
            return observations[0].nrows()
        return observations.nrows()

    def _timestep_tensor_array(self, name, num_timesteps):
        return tf.TensorArray(dtype=self.dtype, size=num_timesteps, name=name)

    def _build_final_step_forward_filter_body(
        self, observations, filter_options, **covariates
    ):
        def body(timestep, prior_mean, prior_cov, cumulative_log_likelihood):

            step_observation = self._step_observation(observations, timestep)
            step_covariates = self._step_covariates(covariates, timestep)

            (
                log_likelihood,
                predicted_mean,
                predicted_cov,
                _,
                _,
            ) = self.forward_filter_step(
                observation=step_observation,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **step_covariates,
            )

            return (
                timestep + 1,
                predicted_mean,
                predicted_cov,
                cumulative_log_likelihood + log_likelihood,
            )

        return body

    def _build_forward_filter_body(self, observations, filter_options, **covariates):
        def body(
            timestep,
            prior_mean,
            prior_cov,
            log_likelihoods,
            predicted_means,
            predicted_cov_diags,
        ):
            step_observation = self._step_observation(observations, timestep)
            step_covariates = self._step_covariates(covariates, timestep)

            (
                log_likelihood,
                predicted_mean,
                predicted_cov,
                _,
                _,
            ) = self.forward_filter_step(
                observation=step_observation,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **step_covariates,
            )

            return (
                timestep + 1,
                predicted_mean,
                predicted_cov,
                log_likelihoods.write(timestep, log_likelihood),
                predicted_means.write(timestep, prior_mean),
                predicted_cov_diags.write(timestep, tfl.diag_part(prior_cov)),
            )

        return body

    def _build_with_predicted_qoi_forward_filter_body(
        self, observations, max_observation_size, filter_options, **covariates
    ):
        def body(
            timestep,
            prior_mean,
            prior_cov,
            log_likelihoods,
            predicted_means,
            predicted_cov_diags,
            predicted_qois,
        ):
            step_observation = self._step_observation(observations, timestep)
            step_covariates = self._step_covariates(covariates, timestep)

            predicted_qoi = util.pad_leading_dimension(
                tensor=self.predict_qoi(prior_mean, prior_cov, **step_covariates),
                size=max_observation_size,
            )

            (
                log_likelihood,
                predicted_mean,
                predicted_cov,
                _,
                _,
            ) = self.forward_filter_step(
                observation=step_observation,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **step_covariates,
            )

            return (
                timestep + 1,
                predicted_mean,
                predicted_cov,
                log_likelihoods.write(timestep, log_likelihood),
                predicted_means.write(timestep, prior_mean),
                predicted_cov_diags.write(timestep, tfl.diag_part(prior_cov)),
                predicted_qois.write(timestep, predicted_qoi),
            )

        return body

    def _build_sample_body(self, num_samples, **covariates):
        def body(
            timestep,
            prior_sample,
            updated_samples,
        ):
            step_covariates = self._step_covariates(covariates, timestep)
            transition_matrix = self.transition_matrix(**step_covariates)
            transition_noise = self.transition_noise(**step_covariates)
            updated_sample = transition_matrix.matvec(
                prior_sample
            ) + transition_noise.sample(num_samples)

            return (
                timestep + 1,
                updated_sample,
                updated_samples.write(timestep, prior_sample),
            )

        return body

    def _build_forward_filter_cond(self, num_timesteps, trace):
        def cond(timestep, *_):
            if trace:
                tf.print("\rtimestep:", timestep, "<", num_timesteps, end="")
            return timestep < num_timesteps

        return cond

    def _final_step_forward_filter_loop(
        self, observations, prior_mean, prior_cov, filter_options, **covariates
    ):
        num_timesteps = self._num_timesteps(observations)

        cond = self._build_forward_filter_cond(num_timesteps, filter_options.trace)

        # the loop body is shared between burnin and "non" burnin stages, this could
        # be optimised for the burnin period to e.g. not actually calculate the
        # cumulative log-likelihood
        body = self._build_final_step_forward_filter_body(
            observations=observations, filter_options=filter_options, **covariates
        )

        if filter_options.burnin_timesteps != 0:
            burnin_loop_vars = (
                tf.constant(0, dtype=num_timesteps.dtype),
                prior_mean,
                prior_cov,
                tf.zeros(shape=self.batch_shape, dtype=self.dtype),
            )

            # new prior mean to start the main loop
            _, prior_mean, prior_cov, _ = tf.while_loop(
                cond=cond,
                body=body,
                loop_vars=burnin_loop_vars,
                maximum_iterations=filter_options.burnin_timesteps,
            )

        loop_vars = (
            tf.constant(filter_options.burnin_timesteps, dtype=num_timesteps.dtype),
            prior_mean,
            prior_cov,
            tf.zeros(shape=self.batch_shape, dtype=self.dtype),
        )

        _, predicted_mean, predicted_cov, cumulative_log_likelihood = tf.while_loop(
            cond=cond, body=body, loop_vars=loop_vars
        )

        return ForwardFilterResults(
            final_step_predicted_mean=predicted_mean,
            final_step_predicted_cov=predicted_cov,
            cumulative_log_likelihood=cumulative_log_likelihood,
        )

    def _forward_filter_loop(
        self, observations, prior_mean, prior_cov, filter_options, **covariates
    ):
        num_timesteps = self._num_timesteps(observations)

        cond = self._build_forward_filter_cond(num_timesteps, filter_options.trace)

        body = self._build_forward_filter_body(
            observations=observations, filter_options=filter_options, **covariates
        )

        loop_vars = (
            tf.constant(0, dtype=num_timesteps.dtype, name="timestep"),
            prior_mean,
            prior_cov,
            self._timestep_tensor_array("log_likelihoods", num_timesteps),
            self._timestep_tensor_array("predicted_means", num_timesteps),
            self._timestep_tensor_array("predicted_cov_diags", num_timesteps),
        )

        (
            _,
            final_step_predicted_mean,
            final_step_predicted_cov,
            log_likelihoods,
            predicted_means,
            predicted_cov_diags,
        ) = tf.while_loop(cond, body, loop_vars)

        # tensor array stack stacks over the first dimension, so the first dimension is
        # time but we want that to be the batch shape so we move dimensions, this is
        # similar to TFP
        return ForwardFilterResults(
            final_step_predicted_mean=final_step_predicted_mean,
            final_step_predicted_cov=final_step_predicted_cov,
            log_likelihoods=distribution_util.move_dimension(
                log_likelihoods.stack(), 0, -1
            ),
            predicted_means=distribution_util.move_dimension(
                predicted_means.stack(), 0, -2
            ),
            predicted_cov_diags=distribution_util.move_dimension(
                predicted_cov_diags.stack(), 0, -2
            ),
        )

    def _with_predicted_qoi_forward_filter_loop(
        self, observations, prior_mean, prior_cov, filter_options, **covariates
    ):
        num_timesteps = self._num_timesteps(observations)

        cond = self._build_forward_filter_cond(num_timesteps, filter_options.trace)

        if isinstance(observations, (tuple, list)):
            observation_sizes = observations[0].row_lengths()
        else:
            observation_sizes = observations.row_lengths()

        body = self._build_with_predicted_qoi_forward_filter_body(
            observations=observations,
            max_observation_size=tf.reduce_max(observation_sizes),
            filter_options=filter_options,
            **covariates,
        )

        loop_vars = (
            tf.constant(0, dtype=num_timesteps.dtype, name="timestep"),
            prior_mean,
            prior_cov,
            self._timestep_tensor_array("log_likelihoods", num_timesteps),
            self._timestep_tensor_array("predicted_means", num_timesteps),
            self._timestep_tensor_array("predicted_cov_diags", num_timesteps),
            self._timestep_tensor_array("predicted_qois", num_timesteps),
        )

        (
            _,
            final_step_predicted_mean,
            final_step_predicted_cov,
            log_likelihoods,
            predicted_means,
            predicted_cov_diags,
            predicted_qois,
        ) = tf.while_loop(cond, body, loop_vars)

        # tensor array stack stacks over the first dimension, so the first dimension is
        # time but we want that to be the batch shape so we move dimensions, this is
        # similar to TFP
        return ForwardFilterResults(
            final_step_predicted_mean=final_step_predicted_mean,
            final_step_predicted_cov=final_step_predicted_cov,
            log_likelihoods=distribution_util.move_dimension(
                log_likelihoods.stack(), 0, -1
            ),
            predicted_means=distribution_util.move_dimension(
                predicted_means.stack(), 0, -2
            ),
            predicted_cov_diags=distribution_util.move_dimension(
                predicted_cov_diags.stack(), 0, -2
            ),
            predicted_qois=tf.RaggedTensor.from_row_lengths(
                util.remove_leading_padding(predicted_qois.concat()), observation_sizes
            ),
        )

    def static_update(
        self,
        num_timesteps: int,
        observations: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
        **covariates,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        """Tuple of (log_likelihood, mean, cov) based on observations[:num_timesteps]"""

        if isinstance(observations, (tuple, list)):
            observation = [x[:num_timesteps].merge_dims(0, 1) for x in observations]
        else:
            observation = observations[:num_timesteps].merge_dims(0, 1)

        step_covariates = {
            k: v[:num_timesteps].merge_dims(0, 1) for k, v in covariates.items()
        }

        (
            log_marginal_likelihood,
            _,
            _,
            filtered_mean,
            filtered_cov,
        ) = self.forward_filter_step(
            observation=observation,
            prior_mean=self.initial_state_prior.mean(),
            prior_cov=self.initial_state_prior.covariance(),
            filter_options=filtering.Options(initial_inverse_hessian_scale=1e-4),
            **step_covariates,
        )

        return log_marginal_likelihood, filtered_mean, filtered_cov

    def forward_filter(
        self,
        observations: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
        prior_mean: Optional[TensorLike] = None,
        prior_cov: Optional[TensorLike] = None,
        filter_options: filtering.Options = filtering.Options(),
        **covariates,
    ) -> ForwardFilterResults:
        """Run filtering for multiple timesteps.

        This is the main entry point to filtering with state space models. This
        functions iterates over each entry in the observations/covariates and records
        details in `ForwardFilterResults`. The algorithm used for filtering depends on
        the state space model class. Gaussian state space models employ the Kalman
        Filter, Generalised state space models the Laplace Gaussian Filter.
        """

        if isinstance(observations, (tuple, list)):
            for i, observation in enumerate(observations):
                tf.debugging.check_numerics(
                    observation, message=f"Checking observations[{i}]"
                )
        else:
            tf.debugging.check_numerics(observations, message="Checking observations")

        for name, covariate in covariates.items():
            if dtype_util.is_floating(covariate.dtype):
                tf.debugging.check_numerics(
                    covariate, message=f"Checking covariate: {name}"
                )

        if filter_options.predict_qoi and filter_options.final_step_only:
            raise ValueError("`predict_qoi` is not compatible with `final_step_only`")

        if filter_options.burnin_timesteps != 0 and not filter_options.final_step_only:
            raise ValueError("`burnin_timesteps` only works with `final_step_only`")

        if prior_mean is None:
            prior_mean = self.initial_state_prior.mean()

        if prior_cov is None:
            prior_cov = self.initial_state_prior.covariance()

        prior_mean = tf.broadcast_to(
            input=prior_mean,
            shape=tf.concat([self.batch_shape, [self.latent_size]], axis=0),
        )

        prior_cov = tf.broadcast_to(
            input=prior_cov,
            shape=tf.concat(
                [self.batch_shape, [self.latent_size, self.latent_size]], axis=0
            ),
        )

        if filter_options.final_step_only:
            output = self._final_step_forward_filter_loop(
                observations=observations,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **covariates,
            )
        elif filter_options.predict_qoi:
            output = self._with_predicted_qoi_forward_filter_loop(
                observations=observations,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **covariates,
            )
        else:
            output = self._forward_filter_loop(
                observations=observations,
                prior_mean=prior_mean,
                prior_cov=prior_cov,
                filter_options=filter_options,
                **covariates,
            )

        if filter_options.trace:
            # add newline after `timestep: x < y` statements in `cond`
            tf.print("\r")

        return output

    def sample_latent_state(
        self,
        num_timesteps: int,
        num_samples: int,
        filter_options: filtering.Options = filtering.Options(),
        **covariates,
    ) -> tf.Tensor:
        """
        Draw samples from the initial latent state prior and run them through
        the transition model without any data to observe their behaviour
        """
        initial_sample = self.initial_state_prior.sample(num_samples)

        cond = self._build_forward_filter_cond(num_timesteps, filter_options.trace)

        body = self._build_sample_body(num_samples, **covariates)

        loop_vars = (
            tf.constant(0, dtype=tf.int32, name="timestep"),
            initial_sample,
            self._timestep_tensor_array("updated_samples", num_timesteps),
        )

        _, _, updated_samples = tf.while_loop(cond, body, loop_vars)

        # tensor array stack stacks over the first dimension, so the first dimension is
        # time but we want that to be the batch shape so we move dimensions, this is
        # similar to TFP
        return distribution_util.move_dimension(updated_samples.stack(), 0, -2)

    def decompose_latent_state(self, latent_state: TensorLike) -> Any:
        """Decompose some conditioned `latent_state` into components"""

        size_splits = self.component_latent_dims

        tensors = tf.split(value=latent_state, num_or_size_splits=size_splits, axis=-1)

        DecomposedLatentState = self._decomposed_latent_state_cls()

        return DecomposedLatentState(*tensors)

    @property
    def batch_shape(self) -> tf.TensorShape:
        """Static shape of a single sample from a single event"""

        return self._batch_shape

    @property
    def initial_state_prior(self) -> tfd.Distribution:
        """Latent state prior distribution"""

        return self._initial_state_prior

    @property
    def dtype(self) -> tf.DType:
        """Model data type"""

        return self._dtype

    @property
    def state_names(self) -> list[str]:
        """List of names for the full latent state vector"""

        return [y for x in self._components for y in x.state_names]

    @property
    def latent_size(self) -> int:
        """Dimension of the latent vector"""

        return self._latent_size

    @property
    def component_latent_dims(self) -> list[int]:
        """List of scalars for the latent dimension for each component"""

        return [x.latent_size for x in self._components]

    @property
    def component_names(self) -> list[str]:
        """List of the names of each component"""

        return [x.name for x in self._components]


class GaussianSSM(AdditiveSSM):
    """State space model with gaussian observation model"""

    def __init__(
        self, components: list[sts.Component], observation_noise_scale: TensorLike
    ):

        dtype = dtype_util.common_dtype(components)

        self._observation_noise_scale = tf.convert_to_tensor(
            observation_noise_scale, dtype=dtype
        )

        super().__init__(
            components=components,
            initial_batch_shape=self._observation_noise_scale.shape,
        )

    def forward_filter_step(
        self,
        observation: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
        prior_mean: TensorLike,
        prior_cov: TensorLike,
        filter_options: filtering.Options = filtering.Options(),
        **step_covariates,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        """Run filtering for one timestep using the KF."""

        observation_size = ps.shape(observation)[0]

        return filtering.kalman_filter_step(
            observation=observation,
            transition_matrix=self.transition_matrix(**step_covariates),
            transition_noise=self.transition_noise(**step_covariates),
            observation_matrix=self.observation_matrix(
                observation_size=observation_size, **step_covariates
            ),
            observation_noise=self.observation_noise(
                observation_size=observation_size, **step_covariates
            ),
            prior_mean=prior_mean,
            prior_cov=prior_cov,
            batch_shape=self.batch_shape,
        )

    def predict_step(
        self, predicted_mean: TensorLike, predicted_cov: TensorLike, **step_covariates
    ) -> tfd.Distribution:

        """single step observation mean and covariance prediction"""

        observation_matrix = self.observation_matrix(**step_covariates)
        observation_noise = self.observation_noise(**step_covariates)

        observation_noise_cov = observation_noise.covariance()

        observation_mean = tfl.matvec(observation_matrix, predicted_mean)
        observation_cov = observation_noise_cov + tf.matmul(
            observation_matrix,
            tf.matmul(predicted_cov, observation_matrix, adjoint_b=True),
        )

        observation_dist = tfd.MultivariateNormalTriL(
            observation_mean, tfl.cholesky(observation_cov)
        )

        return observation_dist

    def observation_noise(self, **step_covariates) -> tfd.Distribution:
        """Observation noise for a single step"""

        return tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=step_covariates["observation_size"],
                multiplier=self.observation_noise_scale,
            )
        )

    @property
    def observation_noise_scale(self) -> tf.Tensor:
        """Scalar observation noise scale"""

        return self._observation_noise_scale


class GeneralisedSSM(AdditiveSSM):
    """State space model with any observation model"""

    def forward_filter_step(
        self,
        observation: Union[TensorLike, list[TensorLike], tuple[TensorLike]],
        prior_mean: TensorLike,
        prior_cov: TensorLike,
        filter_options: filtering.Options = filtering.Options(),
        **step_covariates,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        """Run filtering for one timestep using the LGF."""

        return filtering.laplace_gaussian_step(
            observation_dist_fn=self.make_observation_dist_fn(**step_covariates),
            observation=observation,
            transition_matrix=self.transition_matrix(**step_covariates),
            transition_noise=self.transition_noise(**step_covariates),
            prior_mean=prior_mean,
            prior_cov=prior_cov,
            batch_shape=self.batch_shape,
            options=filter_options,
        )

    def predict_step(
        self,
        predicted_mean: TensorLike,
        predicted_cov: Optional[TensorLike] = None,
        **step_covariates,
    ) -> tfd.Distribution:
        """single step observation predicted distribution via sampling (ideally...)"""

        if predicted_cov is not None:
            warnings.warn("`predicted_cov` is not None, which is unused currently")

        observation_dist_fn = self.make_observation_dist_fn(**step_covariates)

        return observation_dist_fn(predicted_mean)

    def make_observation_dist_fn(self, **step_covariates) -> Callable:
        """A callable `fn(latent_state)` which in turn creates the observation dist"""

        raise NotImplementedError("`make_observation_dist_fn` has not been overriden")
