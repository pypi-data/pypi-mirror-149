"""Get your copula fix here!"""

from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd

# mostly taken from https://www.tensorflow.org/probability/examples/Gaussian_Copula


class NormalTriLCopula(tfd.TransformedDistribution):
    """Distribution over `[0, 1]^k` via transforming a MVN with a Normal CDF."""

    def __init__(
        self,
        loc=None,
        scale_tril=None,
        validate_args=False,
        allow_nan_stats=True,
        name="NormalTriLCopula",
    ):
        """Build a `NormalTriLCopula` distribution."""

        super().__init__(
            distribution=tfd.MultivariateNormalTriL(
                loc=loc,
                scale_tril=scale_tril,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
            ),
            bijector=tfb.NormalCDF(),
            validate_args=validate_args,
            name=name,
        )


class NormalLinearOperatorCopula(tfd.TransformedDistribution):
    """Distribution over `[0, 1]^k` via transforming a MVN with a Normal CDF."""

    def __init__(
        self,
        loc=None,
        scale=None,
        validate_args=False,
        allow_nan_stats=True,
        name="NormalLinearOperatorCopula",
    ):
        """Build a `NormalLinearOperatorCopula` distribution."""

        super().__init__(
            distribution=tfd.MultivariateNormalLinearOperator(
                loc=loc,
                scale=scale,
                validate_args=validate_args,
                allow_nan_stats=allow_nan_stats,
            ),
            bijector=tfb.NormalCDF(),
            validate_args=validate_args,
            name=name,
        )


class CopulaTransformedMultivariateDistribution(tfd.TransformedDistribution):
    """Application of a Copula on a list of target marginals."""

    def __init__(
        self,
        inverse_cdf_marginal_bijectors,
        copula,
        loc=None,
        scale_tril=None,
        validate_args=False,
        name="CopulaTransformedMultivariateDistribution",
    ):
        """Build a `CopulaTransformedMultivariateDistribution` distribution."""

        super().__init__(
            distribution=copula,
            bijector=tfb.Blockwise(
                bijectors=inverse_cdf_marginal_bijectors, validate_args=validate_args
            ),
            validate_args=validate_args,
            name=name,
        )
