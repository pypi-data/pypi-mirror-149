"""Fitting functionality"""

from dataclasses import replace
from enum import Enum

import tensorflow as tf
import tensorflow_probability as tfp

from dyno import filtering
from dyno import finite_differences as fd

tfo = tfp.optimizer

DEFAULT_PARALLEL_ITERATIONS = 10

# TODO(jeff): put these args in dataclasses
# TODO(jeff): add types into this file (must have missed it, oops!)

# override default bfgs args
DEFAULT_INITIAL_INVERSE_HESSIAN_IDENTITY_MULTIPLIER = 1e-3
DEFAULT_TOLERANCE = 1e-4
DEFAULT_X_TOLERANCE = 1e-4
DEFAULT_F_RELATIVE_TOLERANCE = 1e-4

# override default nelder mead args
DEFAULT_POSITION_TOLERANCE = 0.005
DEFAULT_FUNC_TOLERANCE = 0.005

# TODO(jeff): enable tensorboard for fitting


class FitMethod(Enum):
    """Enumeration of methods in the `fit` function"""

    BFGS = "bfgs"
    CENTRAL_DIFFERENCE_BFGS = "central_difference_bfgs"
    FORWARD_DIFFERENCE_BFGS = "forward_difference_bfgs"
    BACKWARD_DIFFERENCE_BFGS = "backward_difference_bfgs"
    NELDER_MEAD = "nelder_mead"
    LOG_PROB_FN = "log_prob_fn"


def bfgs(log_prob_fn, parameters, opt_args, method):
    """Estimate model parameters using BFGS"""

    initial_position = parameters.unconstrained_initial_position

    bfgs_opt_args = opt_args.copy()

    default_initial_inverse_hessian_estimate = (
        tf.eye(tf.shape(initial_position)[-1], dtype=initial_position.dtype)
        * DEFAULT_INITIAL_INVERSE_HESSIAN_IDENTITY_MULTIPLIER
    )

    parallel_iterations = bfgs_opt_args.pop(
        "parallel_iterations", DEFAULT_PARALLEL_ITERATIONS
    )
    initial_inverse_hessian_estimate = bfgs_opt_args.pop(
        "initial_inverse_hessian_estimate", default_initial_inverse_hessian_estimate
    )
    tolerance = bfgs_opt_args.pop("tolerance", DEFAULT_TOLERANCE)
    x_tolerance = bfgs_opt_args.pop("x_tolerance", DEFAULT_X_TOLERANCE)
    f_relative_tolerance = bfgs_opt_args.pop(
        "f_relative_tolerance", DEFAULT_F_RELATIVE_TOLERANCE
    )

    value_and_gradient_fn = {
        FitMethod.BFGS: tfp.math.value_and_gradient,
        FitMethod.CENTRAL_DIFFERENCE_BFGS: fd.value_and_central_difference,
        FitMethod.FORWARD_DIFFERENCE_BFGS: fd.value_and_forward_difference,
        FitMethod.BACKWARD_DIFFERENCE_BFGS: fd.value_and_backward_difference,
    }[method]

    @tf.function(autograph=False)
    def neg_log_prob_and_gradient_fn(x):
        return value_and_gradient_fn(lambda y: -log_prob_fn(y), x)

    return tfo.bfgs_minimize(
        neg_log_prob_and_gradient_fn,
        initial_position=initial_position,
        initial_inverse_hessian_estimate=initial_inverse_hessian_estimate,
        parallel_iterations=parallel_iterations,
        tolerance=tolerance,
        x_tolerance=x_tolerance,
        f_relative_tolerance=f_relative_tolerance,
        **bfgs_opt_args,
    )


def nelder_mead(log_prob_fn, parameters, opt_args):
    """Estimate model parameters using Nelder Mead"""

    initial_vertex = parameters.unconstrained_initial_position

    nelder_mead_opt_args = opt_args.copy()

    func_tolerance = nelder_mead_opt_args.pop("func_tolerance", DEFAULT_FUNC_TOLERANCE)
    position_tolerance = nelder_mead_opt_args.pop(
        "position_tolerance", DEFAULT_POSITION_TOLERANCE
    )
    parallel_iterations = nelder_mead_opt_args.pop(
        "parallel_iterations", DEFAULT_PARALLEL_ITERATIONS
    )

    @tf.function(autograph=False)
    def neg_log_prob_fn(x):
        return -log_prob_fn(x)

    return tfo.nelder_mead_minimize(
        neg_log_prob_fn,
        initial_vertex=initial_vertex,
        func_tolerance=func_tolerance,
        position_tolerance=position_tolerance,
        parallel_iterations=parallel_iterations,
        **nelder_mead_opt_args,
    )


def optimizer_output_to_dict(output, parameters, method):
    """Dict of parameter name -> parameter value for each method"""

    # TODO(jeff): deffo a better way to scale this
    if method in [
        FitMethod.BFGS,
        FitMethod.NELDER_MEAD,
        FitMethod.FORWARD_DIFFERENCE_BFGS,
        FitMethod.BACKWARD_DIFFERENCE_BFGS,
        FitMethod.CENTRAL_DIFFERENCE_BFGS,
    ]:
        constrained_values = parameters.constrain(output.position)
        return {
            k: v.numpy() for k, v in zip(parameters.parameter_names, constrained_values)
        }

    raise ValueError(f"method: {method} not handled")


def fit(
    make_ssm_fn,
    parameters,
    observations,
    covariates,
    method,
    opt_args=None,
    filter_options=filtering.Options(),
    prior_mean=None,
    prior_cov=None,
):
    """High level entry point to parameter estimation"""

    if opt_args is None:
        opt_args = {}

    if method == FitMethod.LOG_PROB_FN:
        apply_constraining_bijector = opt_args["apply_constraining_bijector"]
    else:
        apply_constraining_bijector = True

    filename = f"/tmp/fit-results-{filter_options.uuid}.txt"
    tf.print(f"\nWill save fit results to {filename}\n")

    def log_prob_fn(x):
        """Penalised log likelihood function for SSM parameter estimation"""

        if apply_constraining_bijector:
            x = parameters.constrain(x)

        if filter_options.trace:
            tf.print("parameters:")
            for k, v in zip(parameters.parameter_names, x):
                tf.print("\t", k, v)
                tf.print("\t", k, v, output_stream=f"file://{filename}")

        prior_log_prob = parameters.log_prob(x)

        ssm = make_ssm_fn(*x)

        forward_filter_results = ssm.forward_filter(
            observations=observations,
            prior_mean=prior_mean,
            prior_cov=prior_cov,
            filter_options=replace(filter_options, final_step_only=True),
            **covariates,
        )

        value = prior_log_prob + forward_filter_results.cumulative_log_likelihood

        if filter_options.trace:
            tf.print("log_prob:", value, "\n")
            tf.print("log_prob:", value, "\n", output_stream=f"file://{filename}")
            tf.print(f"Saved to {filename}\n")

        return value

    if method == FitMethod.NELDER_MEAD:
        return nelder_mead(log_prob_fn, parameters, opt_args)

    if method in [
        FitMethod.BFGS,
        FitMethod.CENTRAL_DIFFERENCE_BFGS,
        FitMethod.FORWARD_DIFFERENCE_BFGS,
        FitMethod.BACKWARD_DIFFERENCE_BFGS,
    ]:
        return bfgs(log_prob_fn, parameters, opt_args, method)

    if method == FitMethod.LOG_PROB_FN:
        return log_prob_fn

    raise ValueError(f"method: {method} not handled")
