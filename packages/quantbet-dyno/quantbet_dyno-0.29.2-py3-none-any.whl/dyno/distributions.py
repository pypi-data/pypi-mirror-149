"""Distribution classes and utilities"""

import enum
import functools

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from tensorflow.types.experimental import TensorLike
from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import assert_util
from tensorflow_probability.python.internal import distribution_util
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import prefer_static as ps
from tensorflow_probability.python.internal import reparameterization
from tensorflow_probability.python.internal import tensor_util


def _log_choose(n: TensorLike, k: TensorLike) -> tf.Tensor:
    return -tfp.math.lbeta(1.0 + n - k, 1.0 + k) - tf.math.log1p(n)


def bivariate_values(maximum: int, dtype: tf.DType = tf.int32) -> tf.Tensor:
    """Shape [n, 2] tensor of all 2-way combinations up to `maximum`"""

    seq_len = maximum + 1
    seq = tf.range(seq_len, dtype=dtype)

    x = tf.reshape(tf.tile(seq[:, tf.newaxis], [1, seq_len]), [-1])
    y = tf.tile(seq, [seq_len])

    return tf.stack([x, y], axis=-1)


def bivariate_probs(bivariate_dist: tfd.Distribution, values: TensorLike):
    """prob(values) for a discrete bivariate distribution"""

    # reshape `values` so that it broadcasts with the `batch_shape` of the distribution
    batch_shape = tf.concat(
        [[-1], tf.ones_like(bivariate_dist.batch_shape_tensor()), [2]], axis=0
    )

    return bivariate_dist.prob(
        tf.reshape(tf.cast(values, bivariate_dist.dtype), batch_shape)
    )


def difference_and_total_probs(probs: TensorLike, values: TensorLike) -> tf.Tensor:
    """Tuple of (difference, total) probabilities under some bivariate distribution"""

    x = values[..., 0]
    y = values[..., 1]

    maximum = tf.reduce_max(values)

    difference_probs = tf.math.bincount(x - y + maximum, probs)
    total_probs = tf.math.bincount(x + y, probs)

    # [1, 2, 3, ..., 0] - so we move the first dimension to the end
    perm = tf.concat([tf.range(1, tf.rank(total_probs)), [0]], axis=0)

    return tf.transpose(difference_probs, perm), tf.transpose(total_probs, perm)


class ProbFunction(enum.Enum):

    LOG_PROB = "log_prob"
    WEIGHTED_LOG_PROB = "weighted_log_prob"


class LKJSingle(tfd.TransformedDistribution):
    """The LKJ single/affine transformed Beta distribution"""

    def __init__(
        self,
        concentration: TensorLike,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "LKJSingle",
    ):
        parameters = dict(locals())

        concentration = tf.convert_to_tensor(concentration)

        bijector = tfb.Shift(tf.constant(-1.0, concentration.dtype))(
            tfb.Scale(tf.constant(2.0, concentration.dtype))
        )

        super().__init__(
            distribution=tfd.Beta(
                concentration0=concentration, concentration1=concentration
            ),
            bijector=bijector,
            validate_args=validate_args,
            parameters=parameters,
            name=name,
        )

        self._parameters = parameters

    @classmethod
    def _parameter_properties(cls, dtype, num_classes=None):
        # Because this distribution has different parameters
        # to those in its superclass, we must override this
        # method to prevent tensorflow throwing out nasty
        # warnings.
        return {"concentration": tfp.util.ParameterProperties()}


class WeightedJointDistributionSequential(tfd.JointDistributionSequential):
    """JointDistributionSequential with weights on the log probability parts"""

    def __init__(self, weights: list[float], *args, **kwargs):
        tf.debugging.assert_non_negative(weights, message="weights must be +ve")
        self._weights = weights
        super().__init__(*args, **kwargs)

    def weighted_log_prob(self, value: list[TensorLike]) -> tf.Tensor:
        unweighted_log_prob_parts = self.log_prob_parts(value)

        weighted_log_prob_parts = [
            weight * log_prob
            for weight, log_prob in zip(self.weights, unweighted_log_prob_parts)
        ]

        return sum(weighted_log_prob_parts)

    @property
    def weights(self) -> list[float]:
        return self._weights


class RightCensored(tfd.Distribution):
    """Provides an underlying distribution with (fixed) right censoring"""

    def __init__(
        self,
        underlying_dist: tfd.Distribution,
        censored: TensorLike,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "RightCensoredNormal",
    ):
        parameters = dict(locals())

        self._underlying_dist = underlying_dist
        self._censored = censored

        super().__init__(
            dtype=underlying_dist.dtype,
            reparameterization_type=reparameterization.NOT_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name,
        )

    def _log_prob(self, value):
        return tf.where(
            self.censored,
            self.underlying_dist.log_survival_function(value),
            self.underlying_dist.log_prob(value),
        )

    def _mean(self):
        return self.underlying_dist.mean()

    @property
    def underlying_dist(self):
        return self._underlying_dist

    @property
    def censored(self):
        return self._censored


class BivariatePoisson(tfd.Distribution):
    """A Bivariate Poisson distribution with sum and difference adjustments.
    P(X=i, Y=j) =
    normalizing_constant *
    Poisson(rate1).prob(i) * Poisson(rate2).prob(j) *
    exp(sum_modifier * |(i + j) - (rate1 + rate2)| *
    exp(difference_modifier * |i - j|) *
    exp(equal_modifier * I(i == j)) *
    exp(zeros_modifier * I(i + j == 0)) *
    exp(greater_modifier * I(i > j)) *
    """

    def __init__(
        self,
        log_rates: TensorLike,
        sum_modifier: TensorLike = 0.0,
        difference_modifier: TensorLike = 0.0,
        equal_modifier: TensorLike = 0.0,
        zeros_modifier: TensorLike = 0.0,
        greater_modifier: TensorLike = 0.0,
        maximum_value: int = 25,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "BivariatePoisson",
    ):
        """Initialise Bivariate Poisson distribution."""

        parameters = dict(locals())

        dtype = dtype_util.common_dtype(
            [log_rates, sum_modifier, difference_modifier], dtype_hint=tf.float32
        )

        self._log_rates = tf.convert_to_tensor(log_rates, dtype)
        self._sum_modifier = tf.convert_to_tensor(sum_modifier, dtype)
        self._difference_modifier = tf.convert_to_tensor(difference_modifier, dtype)
        self._equal_modifier = tf.convert_to_tensor(equal_modifier, dtype)
        self._zeros_modifier = tf.convert_to_tensor(zeros_modifier, dtype)
        self._greater_modifier = tf.convert_to_tensor(greater_modifier, dtype)

        self._maximum_value = maximum_value
        self._poisson = tfd.Independent(
            tfd.Poisson(log_rate=self._log_rates), reinterpreted_batch_ndims=1
        )

        super().__init__(
            dtype=dtype,
            reparameterization_type=tfd.NOT_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name,
        )

    @property
    def log_rates(self) -> tf.Tensor:
        return self._log_rates

    @property
    def sum_modifier(self) -> tf.Tensor:
        return self._sum_modifier

    @property
    def difference_modifier(self) -> tf.Tensor:
        return self._difference_modifier

    @property
    def equal_modifier(self) -> tf.Tensor:
        return self._equal_modifier

    @property
    def zeros_modifier(self) -> tf.Tensor:
        return self._zeros_modifier

    @property
    def greater_modifier(self) -> tf.Tensor:
        return self._greater_modifier

    @property
    def maximum_value(self) -> int:
        return self._maximum_value

    def _sum_modification(self, x):
        total_rate = tf.reduce_sum(tf.math.exp(self.log_rates), axis=-1)
        return self.sum_modifier * tf.math.abs(tf.reduce_sum(x, axis=-1) - total_rate)

    def _difference_modification(self, x):
        return self.difference_modifier * tf.math.abs(x[..., 0] - x[..., 1])

    def _equal_modification(self, x):
        return tf.where(tf.equal(x[..., 0], x[..., 1]), self.equal_modifier, 0.0)

    def _zeros_modification(self, x):
        zero = tf.zeros([], x.dtype)
        return tf.where(tf.equal(x[..., 0] + x[..., 1], zero), self.zeros_modifier, 0.0)

    def _greater_modification(self, x):
        return tf.where(tf.greater(x[..., 0], x[..., 1]), self.greater_modifier, 0.0)

    def _log_normalising_constant(self):

        support_shape = tf.concat(
            [[-1], tf.ones_like(self.batch_shape_tensor()), [2]], axis=0
        )

        support = tf.reshape(
            bivariate_values(maximum=self.maximum_value, dtype=self.dtype),
            support_shape,
        )

        unormalised_support_log_probs = self._unnormalised_log_prob(support)

        return tf.reduce_logsumexp(unormalised_support_log_probs, axis=0)

    def _unnormalised_log_prob(self, x):
        return (
            self._poisson.log_prob(x)
            + self._sum_modification(x)
            + self._difference_modification(x)
            + self._equal_modification(x)
            + self._zeros_modification(x)
            + self._greater_modification(x)
        )

    def _log_prob(self, x):
        log_prob = self._unnormalised_log_prob(x) - self._log_normalising_constant()
        return tf.where(
            tf.reduce_any(x > self.maximum_value, axis=-1),
            -tf.constant(np.inf, dtype=self.dtype),
            log_prob,
        )

    def _mean(self):
        support_shape = tf.concat(
            [[-1], tf.ones_like(self.batch_shape_tensor()), [2]], axis=0
        )
        support = tf.reshape(
            bivariate_values(maximum=self.maximum_value, dtype=self.dtype),
            support_shape,
        )

        return tf.reduce_sum(self.prob(support)[..., tf.newaxis] * support, axis=0)

    def _batch_shape_tensor(
        self,
        log_rates=None,
        sum_modifier=None,
        difference_modifier=None,
        equal_modifier=None,
        zeros_modifier=None,
        greater_modifier=None,
    ):
        if log_rates is None:
            log_rates = self.log_rates

        if sum_modifier is None:
            sum_modifier = self.sum_modifier

        if difference_modifier is None:
            difference_modifier = self.difference_modifier

        if equal_modifier is None:
            equal_modifier = self.equal_modifier

        if zeros_modifier is None:
            zeros_modifier = self.zeros_modifier

        if greater_modifier is None:
            greater_modifier = self.greater_modifier

        return functools.reduce(
            ps.broadcast_shape,
            [
                ps.shape(log_rates)[:-1],
                ps.shape(sum_modifier),
                ps.shape(difference_modifier),
                ps.shape(equal_modifier),
                ps.shape(zeros_modifier),
                ps.shape(greater_modifier),
            ],
        )

    def _batch_shape(self):
        return functools.reduce(
            tf.broadcast_static_shape,
            [
                self.log_rates.shape[:-1],
                self.sum_modifier.shape,
                self.difference_modifier.shape,
                self.equal_modifier.shape,
                self.zeros_modifier.shape,
                self.greater_modifier.shape,
            ],
        )

    def _event_shape_tensor(self):
        return tf.constant([2], dtype=tf.int32)

    def _event_shape(self):
        return tf.TensorShape([2])

    def _parameter_control_dependencies(self, is_init):
        assertions = []

        if is_init:
            float_msg = "Argument `{}` must have floating type."

            if not dtype_util.is_floating(self.log_rates.dtype):
                raise TypeError(float_msg.format("log_rates"))

            if not dtype_util.is_floating(self.sum_modifier.dtype):
                raise TypeError(float_msg.format("sum_modifier"))

            if not dtype_util.is_floating(self.difference_modifier.dtype):
                raise TypeError(float_msg.format("difference_modifier"))

            if not dtype_util.is_floating(self.equal_modifier.dtype):
                raise TypeError(float_msg.format("equal_modifier"))

            if not dtype_util.is_floating(self.zeros_modifier.dtype):
                raise TypeError(float_msg.format("zeros_modifier"))

            if not dtype_util.is_floating(self.greater_modifier.dtype):
                raise TypeError(float_msg.format("greater_modifier"))

            log_rates_shape = self.log_rates.shape
            shape_msg = "Argument `log_rates` must have a rightmost shape of 2."
            if log_rates_shape is not None:
                if log_rates_shape[-1] != 2:
                    raise ValueError(shape_msg)
            elif self.validate_args:
                log_rates_shape = tf.shape(self.log_rates)
                assertions.append(
                    assert_util.assert_equal(log_rates_shape[-1], 2, message=shape_msg)
                )

        if not self.validate_args:
            return []

        return assertions

    def _sample_n(self, n, seed=None):
        support = bivariate_values(maximum=self.maximum_value, dtype=self.dtype)

        log_prob_support_shape = tf.concat(
            [[-1], tf.ones_like(self.batch_shape_tensor()), [2]], axis=0
        )
        log_prob_support = tf.reshape(support, log_prob_support_shape)

        logits = distribution_util.move_dimension(
            self._unnormalised_log_prob(log_prob_support), 0, -1
        )

        samples = tfd.Categorical(logits=logits).sample(n, seed)

        return tf.gather(support, samples)


class GeometricPoisson(tfd.Distribution):
    """The Geometric Poisson distribution"""

    # TODO: if we decide to use this, it needs testing

    def __init__(
        self,
        rate: TensorLike,
        prob: TensorLike,
        dtype: tf.DType = tf.int32,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "GeometricPoisson",
    ):
        parameters = dict(locals())

        self._float_dtype = dtype_util.common_dtype([rate, prob], dtype_hint=tf.float32)
        self._rate = tf.convert_to_tensor(rate, dtype=self._float_dtype)
        self._prob_parameter = tf.convert_to_tensor(prob, dtype=self._float_dtype)

        super().__init__(
            dtype=dtype,
            reparameterization_type=tfd.NOT_REPARAMETERIZED,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            parameters=parameters,
            name=name,
        )

    @property
    def rate(self) -> tf.Tensor:
        return self._rate

    @property
    def prob_parameter(self) -> tf.Tensor:
        return self._prob_parameter

    def _log_prob(self, x):
        x_float = tf.cast(x, dtype=self._float_dtype)
        num_terms = tf.reduce_max(x)
        seq = tf.range(1, num_terms + 1, dtype=self._float_dtype)
        poisson = tfd.Poisson(rate=self.rate[..., tf.newaxis])
        terms = (
            poisson.log_prob(seq)
            + (x_float[..., tf.newaxis] - seq) * tf.math.log1p(-self.prob_parameter)
            + seq * tf.math.log(self.prob_parameter)
            + _log_choose(tf.maximum(x_float[..., tf.newaxis] - 1.0, 0.0), seq - 1.0)
        )
        return tf.where(x == 0, -self.rate, tf.math.reduce_logsumexp(terms, axis=-1))

    def _batch_shape_tensor(self, prob=None, rate=None):
        prob = self.prob_parameter if prob is None else prob
        rate = self.rate if rate is None else rate
        return ps.broadcast_shape(ps.shape(prob), ps.shape(rate))

    def _batch_shape(self):
        return tf.broadcast_static_shape(self.rate.shape, self.prob_parameter.shape)

    def _event_shape_tensor(self):
        return tf.constant([], dtype=tf.int32)

    def _event_shape(self):
        return tf.TensorShape([])

    def _parameter_control_dependencies(self, is_init):

        if is_init:
            if not dtype_util.is_floating(self.rate.dtype):
                raise TypeError("Argument `rate` must having floating type.")
            if not dtype_util.is_floating(self.prob_parameter.dtype):
                raise TypeError("Argument `prob` must having floating type.")

        if not self.validate_args:
            return []

        assertions = []

        if is_init != tensor_util.is_ref(self.prob_parameter):
            prob = tf.convert_to_tensor(self.prob_parameter)
            assertions += [
                assert_util.assert_non_negative(
                    prob, message="prob has components less than 0"
                ),
                assert_util.assert_less_equal(
                    prob,
                    tf.constant(1.0, dtype=prob.dtype),
                    message="prob has components greater than 1",
                ),
            ]
        if is_init != tensor_util.is_ref(self.rate):
            rate = tf.convert_to_tensor(self.rate)
            assertions += [
                assert_util.assert_non_negative(
                    rate, message="Argument `rate` must be non-negative."
                )
            ]

        return assertions


class CumulativeNormal(tfd.MultivariateNormalTriL):
    """MVN of cumulative sum of independant Normals with same scale and loc 0."""

    def __init__(
        self,
        dimension: int,
        scale: TensorLike,
        validate_args: bool = False,
        allow_nan_stats: bool = True,
        name: str = "CumulativeNormal",
    ):

        scale = tf.convert_to_tensor(scale)

        self._dimension = dimension
        self._scale = scale

        num_scale_tril_values = dimension * (dimension + 1) // 2
        scale_tril = tfp.math.fill_triangular(
            tf.tile(
                scale[..., tf.newaxis],
                tf.concat(
                    [tf.ones_like(ps.shape(scale)), [num_scale_tril_values]], axis=0
                ),
            )
        )

        super().__init__(
            loc=0.0,
            scale_tril=scale_tril,
            validate_args=validate_args,
            allow_nan_stats=allow_nan_stats,
            name=name,
        )

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def scale(self) -> tf.Tensor:
        return self._scale
