"""Structural time series components"""

import abc
import functools
from itertools import chain

from typing import Optional

import tensorflow as tf

from tensorflow import linalg as tfl, TensorShape
from tensorflow.types.experimental import TensorLike
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import prefer_static as ps

from dyno import distributions as dist
from dyno import linalg
from dyno import math

# TODO(jeff): add doc for each component


def build_multi_categorical_transition_noise(
    num_categories: int, drift_scale: TensorLike, drift_correlation_matrix: TensorLike
) -> tfd.Distribution:
    """Transition noise MVN for the multi categorical component"""

    single_team_covariance_matrix = tfl.LinearOperatorFullMatrix(
        linalg.build_covariance_matrix(drift_correlation_matrix, drift_scale),
        is_non_singular=True,
        is_self_adjoint=True,
        is_positive_definite=True,
        is_square=True,
    )

    # properties are inferred from the inputs
    covariance_matrix = tfl.LinearOperatorBlockDiag(
        [single_team_covariance_matrix] * num_categories, is_square=True
    )

    return tfd.MultivariateNormalLinearOperator(scale=tfl.cholesky(covariance_matrix))


def build_autoregressive_transition_matrix(
    coefficients: TensorLike,
) -> tfl.LinearOperator:
    """Transition matrix for the autoregressive component"""

    top_row = tf.expand_dims(coefficients, -2)
    coef_shape = ps.shape(coefficients)
    batch_shape, order = coef_shape[:-1], coef_shape[-1]
    remaining_rows = tf.concat(
        [
            tf.eye(order - 1, dtype=coefficients.dtype, batch_shape=batch_shape),
            tf.zeros(
                tf.concat([batch_shape, (order - 1, 1)], axis=0),
                dtype=coefficients.dtype,
            ),
        ],
        axis=-1,
    )
    return tfl.LinearOperatorFullMatrix(tf.concat([top_row, remaining_rows], axis=-2))


def build_autoregressive_transition_noise(
    drift_scale: TensorLike,
    order: int,
) -> tfd.MultivariateNormalLinearOperator:
    return tfd.MultivariateNormalLinearOperator(
        scale=tfl.LinearOperatorDiag(
            diag=tf.stack(
                [drift_scale] + [tf.zeros_like(drift_scale)] * (order - 1), axis=-1
            )
        )
    )


def build_categorical_autoregressive_transition_matrix(
    num_categories: int,
    coefficients: TensorLike,
) -> tfl.LinearOperatorBlockDiag:
    """Transition matrix for the CategoricalAutoregressive component"""
    single_component_transition_matrix = build_autoregressive_transition_matrix(
        coefficients
    )

    out = tfl.LinearOperatorBlockDiag(
        [single_component_transition_matrix] * num_categories, is_square=True
    )
    return out


def build_categorical_autoregressive_transition_noise(
    num_categories: int,
    drift_scale: TensorLike,
    order: int,
) -> tfd.MultivariateNormalLinearOperator:
    """Transition noise distribution for the CategoricalAutoregressive component"""
    single_component_noise = build_autoregressive_transition_noise(drift_scale, order)
    single_component_scale = single_component_noise.scale

    scale = tfl.LinearOperatorBlockDiag(
        [single_component_scale] * num_categories, is_square=True
    )

    out = tfd.MultivariateNormalLinearOperator(scale=scale)
    return out


def build_local_linear_trend_transition_matrix(
    dtype: TensorLike,
    slope_decay: float = 1.0,
) -> tfl.LinearOperator:
    """Transition matrix for the LocalLinearTrend component"""
    return tfl.LinearOperatorFullMatrix(
        tf.cast(
            tf.stack(
                [
                    [1, 1],
                    [0, slope_decay],
                ]
            ),
            dtype=dtype,
        )
    )


def build_local_linear_trend_transition_noise(
    level_drift_scale: TensorLike,
    slope_drift_scale: TensorLike,
    parameter_batch_shape: TensorShape,
) -> tfd.MultivariateNormalDiag:
    """Transition noise distribution for the LocalLinearTrend component"""
    return tfd.MultivariateNormalDiag(
        scale_diag=tf.stack(
            [
                tf.broadcast_to(level_drift_scale, parameter_batch_shape),
                tf.broadcast_to(slope_drift_scale, parameter_batch_shape),
            ],
            axis=-1,
        )
    )


def build_categorical_local_linear_trend_transition_matrix(
    num_categories: int,
    dtype: TensorLike,
    slope_decay: float = 1.0,
) -> tfl.LinearOperator:
    """Transition matrix for the CategoricalLocalLinearTrend component"""
    single_component_transition_matrix = build_local_linear_trend_transition_matrix(
        dtype,
        slope_decay,
    )
    out = tfl.LinearOperatorBlockDiag(
        [single_component_transition_matrix] * num_categories, is_square=True
    )
    return out


def build_categorical_local_linear_trend_transition_noise(
    num_categories: int,
    level_drift_scale: TensorLike,
    slope_drift_scale: TensorLike,
    parameter_batch_shape: TensorShape,
) -> tfd.MultivariateNormalLinearOperator:
    """Transition noise distribution for the CategoricalLocalLinearTrend component"""
    single_component_noise = build_local_linear_trend_transition_noise(
        level_drift_scale,
        slope_drift_scale,
        parameter_batch_shape,
    )
    single_component_scale = single_component_noise.scale

    scale = tfl.LinearOperatorBlockDiag(
        [single_component_scale] * num_categories, is_square=True
    )

    out = tfd.MultivariateNormalLinearOperator(scale=scale)
    return out


class Component(abc.ABC):
    """structural time series component"""

    def __init__(
        self,
        name: str,
        latent_size: int,
        initial_state_prior: tfd.Distribution,
        batch_shape: tf.TensorShape,
        dtype: tf.DType,
    ):
        self._name = name
        self._latent_size = latent_size
        self._initial_state_prior = initial_state_prior
        self._batch_shape = batch_shape
        self._dtype = dtype

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        # doesn't make sense for some components so don't make it a requirement
        raise NotImplementedError

    @abc.abstractmethod
    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        pass

    @abc.abstractmethod
    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        pass

    @property
    def batch_shape(self) -> tf.TensorShape:
        return self._batch_shape

    @property
    def state_names(self) -> list[str]:
        if tf.equal(self.latent_size, 1):
            return [self.name]
        return [f"{self.name}[{x}]" for x in range(self.latent_size)]

    @property
    def initial_state_prior(self) -> tfd.Distribution:
        return self._initial_state_prior

    @property
    def name(self) -> str:
        return self._name

    @property
    def latent_size(self) -> int:
        return self._latent_size

    @property
    def dtype(self) -> tf.DType:
        return self._dtype


class LocalLevel(Component):
    """local level structural time series component"""

    def __init__(
        self,
        name: str,
        drift_scale: TensorLike,
        latent_size: int = 1,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=latent_size, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=latent_size, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=latent_size, multiplier=drift_scale
            )
        )

        super().__init__(
            name=name,
            latent_size=latent_size,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        # only makes sense for latent size 1 in gaussian case which uses the
        # observation_matrix
        return tf.ones([step_covariates["observation_size"], 1], dtype=self.dtype)

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise


class Autoregressive(Component):
    """autoregressive structural time series component"""

    def __init__(
        self,
        name: str,
        coefficients: TensorLike,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        dtype = dtype_util.common_dtype(
            [coefficients, drift_scale], dtype_hint=tf.float32
        )

        coefficients = tf.convert_to_tensor(coefficients, dtype=dtype)
        drift_scale = tf.convert_to_tensor(drift_scale, dtype=dtype)

        order = coefficients.shape[-1]

        if order is None:
            raise ValueError("Autoregressive coefficients must have static shape")

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=order, dtype=dtype)
            )

        self._order = order

        self._transition_matrix = build_autoregressive_transition_matrix(coefficients)

        self._transition_noise = build_autoregressive_transition_noise(
            drift_scale, order
        )

        super().__init__(
            name=name,
            latent_size=order,
            dtype=dtype,
            batch_shape=functools.reduce(
                tf.broadcast_static_shape,
                [
                    self._transition_matrix.batch_shape,
                    self._transition_noise.batch_shape,
                    initial_state_prior.batch_shape,
                ],
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        observation_size = step_covariates["observation_size"]
        return tf.concat(
            [
                tf.ones([observation_size, 1], dtype=self.dtype),
                tf.zeros([observation_size, self._order - 1], dtype=self.dtype),
            ],
            axis=1,
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise


class DynamicRegression(Component):
    """dynamic regression structural time series component"""

    def __init__(
        self,
        name: str,
        latent_size: int,
        drift_scale: TensorLike,
        state_names: list[str] = None,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        if state_names is None:
            state_names = [str(x) for x in range(latent_size)]

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=latent_size, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=latent_size, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=latent_size, multiplier=drift_scale
            )
        )

        self._state_names = state_names

        super().__init__(
            name=name,
            latent_size=latent_size,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        design_matrix = tf.reshape(step_covariates[self.name], [-1, self.latent_size])
        return design_matrix

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def state_names(self):
        if tf.equal(self.latent_size, 1):
            return [self.name]
        return [f"{self.name}[{x}]" for x in self._state_names]


class Categorical(Component):
    """categorical structural time series component"""

    def __init__(
        self,
        name: str,
        categories,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype
        num_categories = len(categories)

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=num_categories, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=num_categories, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=num_categories, multiplier=drift_scale
            )
        )

        self._num_categories = num_categories
        self._categories = categories

        super().__init__(
            name=name,
            latent_size=num_categories,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        return tf.one_hot(
            step_covariates[self.name], self.latent_size, dtype=self.dtype
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def num_categories(self):
        return self._num_categories

    @property
    def categories(self):
        return self._categories

    @property
    def state_names(self):
        return [f"{self.name}[{x}]" for x in self.categories]


# TODO: The current Categorical class is really a
#       CategoricalLocalLevel class. All the internals
#       match up with having a LocalLevel per category.
#       Perhaps it should be renamed as such.

# TODO: It would be nice if we could rearrange things
#       so the Categorical class was a sort of wrapper
#       which could take in any single component as
#       an argument, rather than re-defining different
#       types of Categorical class, but for now this
#       is simpler.
class CategoricalLocalLinearTrend(Component):
    """categorical structural time series component"""

    def __init__(
        self,
        name: str,
        categories,
        level_drift_scale: TensorLike,
        slope_drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
        slope_decay: float = 1.0,
    ):
        dtype = dtype_util.common_dtype(
            [level_drift_scale, slope_drift_scale], dtype_hint=tf.float32
        )

        level_drift_scale = tf.convert_to_tensor(level_drift_scale, dtype=dtype)
        slope_drift_scale = tf.convert_to_tensor(slope_drift_scale, dtype=dtype)

        num_categories = len(categories)
        latent_size = 2 * num_categories  # one for levels, one for slopes

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=latent_size, dtype=dtype)
            )

        parameter_batch_shape = ps.broadcast_shape(
            ps.shape(level_drift_scale), ps.shape(slope_drift_scale)
        )
        err = (
            f"No broadcasting of parameters is supported yet ({parameter_batch_shape})"
            # This can be added later if we want
        )
        assert parameter_batch_shape.as_list() == [], err

        self._transition_matrix = (
            build_categorical_local_linear_trend_transition_matrix(
                num_categories,
                dtype,
                slope_decay,
            )
        )

        self._transition_noise = build_categorical_local_linear_trend_transition_noise(
            num_categories,
            level_drift_scale,
            slope_drift_scale,
            parameter_batch_shape,
        )

        self._num_categories = num_categories
        self._categories = categories

        super().__init__(
            name=name,
            latent_size=latent_size,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        raise NotImplementedError

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def num_categories(self):
        return self._num_categories

    @property
    def categories(self):
        return self._categories

    @property
    def state_names(self) -> list[str]:
        list_of_lists = [[f"level[{x}]", f"slope[{x}]"] for x in self.categories]
        return list(chain(*list_of_lists))


class CategoricalAutoregressive(Component):
    """Categorical auto-regressive structural time series component"""

    def __init__(
        self,
        name: str,
        categories,
        coefficients: TensorLike,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):
        dtype = dtype_util.common_dtype(
            [coefficients, drift_scale], dtype_hint=tf.float32
        )

        coefficients = tf.convert_to_tensor(coefficients, dtype=dtype)
        drift_scale = tf.convert_to_tensor(drift_scale, dtype=dtype)

        order = coefficients.shape[-1]

        num_categories = len(categories)
        latent_size = num_categories * order

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=latent_size, dtype=dtype)
            )

        self._order = order

        self._transition_matrix = build_categorical_autoregressive_transition_matrix(
            num_categories,
            coefficients,
        )

        self._transition_noise = build_categorical_autoregressive_transition_noise(
            num_categories,
            drift_scale,
            order,
        )

        self._num_categories = num_categories
        self._categories = categories

        batch_shape = functools.reduce(
            tf.broadcast_static_shape,
            [
                self._transition_matrix.batch_shape,
                self._transition_noise.batch_shape,
                initial_state_prior.batch_shape,
            ],
        )
        err = (
            f"No broadcasting of parameters is supported yet ({batch_shape})"
            # This can be added later if we want
        )
        assert batch_shape == [], err

        super().__init__(
            name=name,
            latent_size=latent_size,
            dtype=dtype,
            batch_shape=batch_shape,
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        raise NotImplementedError

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    def num_categories(self):
        return self._num_categories

    @property
    def categories(self):
        return self._categories

    @property
    def state_names(self) -> list[str]:
        if self._order == 1:
            return [f"cat_ar1[{x}]" for x in self.categories]
        else:
            return [
                f"cat_ar{self._order}[{x}[{i}]]"
                for x in self.categories
                for i in range(self._order)
            ]


class CategoricalDifference(Component):
    """categorical difference structural time series component"""

    def __init__(
        self,
        name: str,
        x,
        y,
        categories,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype
        num_categories = len(categories)

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=num_categories, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=num_categories, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=num_categories, multiplier=drift_scale
            )
        )

        self._x = x
        self._y = y
        self._num_categories = num_categories
        self._categories = categories

        super().__init__(
            name=name,
            latent_size=num_categories,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        x = tf.one_hot(step_covariates[self._x], self.num_categories, dtype=self.dtype)
        y = tf.one_hot(step_covariates[self._y], self.num_categories, dtype=self.dtype)
        return x - y

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def num_categories(self):
        return self._num_categories

    @property
    def categories(self):
        return self._categories

    @property
    def state_names(self):
        return [f"{self.name}[{x}]" for x in self.categories]


class CategoricalSum(Component):
    """categorical sum structural time series component"""

    def __init__(
        self,
        name: str,
        categories,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype
        num_categories = len(categories)

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=num_categories, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=num_categories, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=num_categories, multiplier=drift_scale
            )
        )

        self._num_categories = num_categories
        self._categories = categories

        super().__init__(
            name=name,
            latent_size=num_categories,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        return tf.reduce_max(
            tf.one_hot(step_covariates[self.name], self._num_categories), axis=1
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def num_categories(self) -> int:
        return self._num_categories

    @property
    def categories(self) -> list[str]:
        return self._categories

    @property
    def state_names(self) -> list[str]:
        return [f"{self.name}[{x}]" for x in self.categories]


class CategoricalSumDifference(Component):
    """diff of categorical sum structural time series component"""

    def __init__(
        self,
        name: str,
        x,
        y,
        categories,
        drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):

        drift_scale = tf.convert_to_tensor(drift_scale)
        dtype = drift_scale.dtype
        num_categories = len(categories)

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=num_categories, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=num_categories, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorScaledIdentity(
                num_rows=num_categories, multiplier=drift_scale
            )
        )

        self._x = x
        self._y = y
        self._num_categories = num_categories
        self._categories = categories

        super().__init__(
            name=name,
            latent_size=num_categories,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        x = tf.reduce_max(
            tf.one_hot(step_covariates[self._x], self._num_categories), axis=1
        )
        y = tf.reduce_max(
            tf.one_hot(step_covariates[self._y], self._num_categories), axis=1
        )
        return x - y

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def num_categories(self) -> int:
        return self._num_categories

    @property
    def categories(self) -> list[str]:
        return self._categories

    @property
    def state_names(self) -> list[str]:
        return [f"{self.name}[{x}]" for x in self.categories]


class MultiCategorical(Component):
    """Many self correlated categorical components"""

    def __init__(
        self,
        name: str,
        categories: list[str],
        sub_component_names: list[str],
        drift_scale: TensorLike,
        drift_correlation_matrix: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
    ):
        dtype = dtype_util.common_dtype(
            [drift_scale, drift_correlation_matrix], dtype_hint=tf.float32
        )

        drift_scale = tf.convert_to_tensor(drift_scale, dtype=dtype)
        drift_correlation_matrix = tf.convert_to_tensor(
            drift_correlation_matrix, dtype=dtype
        )

        num_categories = len(categories)
        num_sub_components = len(sub_component_names)

        latent_size = num_sub_components * num_categories

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=latent_size, dtype=dtype)
            )

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=latent_size, dtype=dtype
        )

        self._transition_noise = build_multi_categorical_transition_noise(
            num_categories=num_categories,
            drift_scale=drift_scale,
            drift_correlation_matrix=drift_correlation_matrix,
        )

        self._num_categories = num_categories
        self._categories = categories
        self._sub_component_names = sub_component_names
        self._num_sub_components = num_sub_components

        super().__init__(
            name=name,
            latent_size=latent_size,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    def observation_matrix(self, **step_covariates) -> tf.Tensor:

        design_matrices = [
            tf.one_hot(step_covariates[x], self.num_categories, dtype=self.dtype)
            for x in self.sub_component_names
        ]

        return linalg.interleave_matrix_columns(design_matrices)

    @property
    def num_sub_components(self) -> int:
        return self._num_sub_components

    @property
    def sub_component_names(self) -> list[str]:
        return self._sub_component_names

    @property
    def num_categories(self) -> int:
        return self._num_categories

    @property
    def categories(self) -> list[str]:
        return self._categories

    @property
    def state_names(self) -> list[str]:
        return [
            f"{sub_component_name}[{category}]"
            for category in self.categories
            for sub_component_name in self.sub_component_names
        ]


class BSpline(Component):
    """B-Spline structural time series component"""

    def __init__(self, name: str, scale: TensorLike, b_spline: math.BSpline):

        if b_spline.intercept:
            raise ValueError("sts.BSpline does not work with `intercept=True`")

        scale = tf.convert_to_tensor(scale)
        dtype = scale.dtype

        initial_state_prior = dist.CumulativeNormal(dimension=b_spline.df, scale=scale)

        self._transition_matrix = tfl.LinearOperatorIdentity(
            num_rows=b_spline.df, dtype=dtype
        )

        self._transition_noise = tfd.MultivariateNormalLinearOperator(
            scale=tfl.LinearOperatorZeros(num_rows=b_spline.df, dtype=dtype)
        )

        self._b_spline = b_spline

        super().__init__(
            name=name,
            latent_size=b_spline.df,
            dtype=dtype,
            batch_shape=initial_state_prior.batch_shape,
            initial_state_prior=initial_state_prior,
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def b_spline(self) -> math.BSpline:
        return self._b_spline


class LocalLinearTrend(Component):
    """local linear trend time series component"""

    def __init__(
        self,
        name: str,
        level_drift_scale: TensorLike,
        slope_drift_scale: TensorLike,
        initial_state_prior: Optional[tfd.Distribution] = None,
        slope_decay: float = 1.0,
    ):
        """

        Args:
          name:
          level_drift_scale:
          slope_drift_scale:
          initial_state_prior:
          slope_decay:
            Entry in the transition matrix for the
            relationship between slope_t and slope_{t-1}.
            Defaults to 1.0 but in some cases it might
            make sense for the slope to decay to 0 over
            time, in which case use 0 < slope_decay < 1.
        """
        dtype = dtype_util.common_dtype(
            [level_drift_scale, slope_drift_scale], dtype_hint=tf.float32
        )

        level_drift_scale = tf.convert_to_tensor(level_drift_scale, dtype=dtype)
        slope_drift_scale = tf.convert_to_tensor(slope_drift_scale, dtype=dtype)

        if initial_state_prior is None:
            initial_state_prior = tfd.MultivariateNormalLinearOperator(
                scale=tfl.LinearOperatorIdentity(num_rows=2, dtype=dtype)
            )

        parameter_batch_shape = ps.broadcast_shape(
            ps.shape(level_drift_scale), ps.shape(slope_drift_scale)
        )

        self._transition_matrix = build_local_linear_trend_transition_matrix(
            dtype,
            slope_decay,
        )

        self._transition_noise = build_local_linear_trend_transition_noise(
            level_drift_scale,
            slope_drift_scale,
            parameter_batch_shape,
        )

        self._observation_matrix = tf.constant([[1.0, 0.0]], dtype=dtype)

        super().__init__(
            name=name,
            latent_size=2,
            dtype=dtype,
            batch_shape=tf.broadcast_static_shape(
                self._transition_noise.batch_shape, initial_state_prior.batch_shape
            ),
            initial_state_prior=initial_state_prior,
        )

    def observation_matrix(self, **step_covariates) -> tf.Tensor:
        observation_size = step_covariates["observation_size"]
        return tf.stack(
            [
                tf.ones([observation_size], dtype=self.dtype),
                tf.zeros([observation_size], dtype=self.dtype),
            ],
            axis=-1,
        )

    def transition_matrix(self, **step_covariates) -> tfl.LinearOperator:
        return self._transition_matrix

    def transition_noise(self, **step_covariates) -> tfd.Distribution:
        return self._transition_noise

    @property
    def state_names(self) -> list[str]:
        return [f"{self.name}[level]", f"{self.name}[slope]"]
