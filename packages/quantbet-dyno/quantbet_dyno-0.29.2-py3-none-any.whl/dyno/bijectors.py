"""Bijector things, whatever they are."""

import numpy as np
import tensorflow as tf

from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import prefer_static as ps


class InverseCDF(tfb.Bijector):
    def __init__(self, distribution, validate_args=False, name="InverseCDF"):

        parameters = dict(locals())

        self._distribution = distribution

        super().__init__(
            validate_args=validate_args,
            dtype=distribution.dtype,
            forward_min_event_ndims=0,
            parameters=parameters,
            name=name,
        )

    def _forward(self, y):
        return self._distribution.quantile(y)

    def _inverse(self, x):
        return self._distribution.cdf(x)

    def _inverse_log_det_jacobian(self, x):
        return self._distribution.log_prob(x)

    @property
    def distribution(self):
        return self._distribution

    @classmethod
    def _is_increasing(cls):
        return True

    @classmethod
    def _parameter_properties(cls, dtype):
        return dict()


class InverseNormalCDF(InverseCDF):
    def __init__(
        self, loc=0.0, scale=1.0, validate_args=False, name="InverseNormalCDF"
    ):

        super().__init__(
            distribution=tfd.Normal(loc=loc, scale=scale, validate_args=validate_args),
            validate_args=validate_args,
            name=name,
        )


class InversePoissonCDF(InverseCDF):
    def __init__(
        self,
        rate=None,
        log_rate=None,
        max_value=100,
        validate_args=False,
        name="InversePoissonCDF",
    ):

        self._max_value = max_value

        super().__init__(
            distribution=tfd.Poisson(
                rate=rate,
                log_rate=log_rate,
                validate_args=validate_args,
            ),
            validate_args=validate_args,
            name=name,
        )

    def _forward(self, y):
        y = tf.convert_to_tensor(y)
        dist = self.distribution
        dtype = dist.dtype
        broadcast_shape = ps.broadcast_shape(ps.shape(y), dist.batch_shape_tensor())
        values_shape = tf.concat([[-1], tf.ones_like(broadcast_shape)], axis=0)
        values = tf.reshape(tf.range(self.max_value, dtype=dtype), values_shape)
        probs = dist.cdf(values)
        probs_gt = probs > y

        return tf.where(
            tf.reduce_any(probs_gt, axis=0),
            tf.cast(tf.argmax(probs_gt, axis=0), dtype),
            tf.constant(np.inf, dtype),
        )

    @property
    def max_value(self):
        return self._max_value

    @property
    def _is_injective(self):
        # this stops a lot of stuff "working" but is actually true for this "bijector"
        return False
