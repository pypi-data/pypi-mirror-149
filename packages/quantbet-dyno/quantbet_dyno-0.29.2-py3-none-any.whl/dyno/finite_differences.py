"""Approximate gradients using finite difference methods"""

from typing import Callable
from typing import Optional

import numpy as np
import tensorflow as tf

from tensorflow.types.experimental import TensorLike


def _step_sizes(position, fn):
    dtype = position.dtype
    machine_epsilon = tf.constant(np.finfo(dtype.as_numpy_dtype).eps, dtype=dtype)
    unit_roundoff = machine_epsilon / 2.0
    min_step_size = fn(unit_roundoff)
    scaled_step_size = tf.abs(position) * min_step_size

    return tf.maximum(min_step_size, scaled_step_size)


def step_sizes_one_sided(position: TensorLike) -> tf.Tensor:
    """Step size (h) used in forward/backward difference, max(sqrt(u), |x| * sqrt(u))

    `u` is the so-called "unit roundoff"

    references:
    - https://quant-bet.atlassian.net/l/c/9zXzt50v, Numerical Optimization section 8.1
    - https://en.wikipedia.org/wiki/Machine_epsilon
    """
    return _step_sizes(position, tf.sqrt)


def step_sizes_central(position: TensorLike) -> tf.Tensor:
    """Step size (h) used in central difference, max(cbrt(u), |x| * cbrt(u))

    `u` is the so-called "unit roundoff"

    references:
    - https://quant-bet.atlassian.net/l/c/9zXzt50v, Numerical Optimization section 8.1
    - https://en.wikipedia.org/wiki/Machine_epsilon
    """
    return _step_sizes(position, lambda x: tf.math.pow(x, 1.0 / 3.0))


def evaluation_points_one_sided(
    position: TensorLike, step_sizes: TensorLike, fn: Callable
) -> tf.Tensor:
    """Shape [dim + 1, dim] Tensor of points required for forward/backward difference

    For `i` in `range(dim)` this functions returns `points` s.t.:

    points[i] = position + step[i]

    and in the last index:

    points[dim] = position

    where `step` is a tensor of shape `[dim]` with a single non-zero element in index
    `i` with value `step_sizes[i]`.

    `fn` should be `tf.tensor_scatter_nd_add` for forward difference or
    `tf.tensor_scatter_nd_sub` for backward difference.
    """

    dim = tf.shape(position)[0]

    return fn(
        tensor=tf.tile(position[tf.newaxis, ...], [dim + 1, 1]),
        indices=tf.tile(tf.range(dim)[..., tf.newaxis], [1, 2]),
        updates=step_sizes,
    )


def evaluation_points_central(
    position: TensorLike, step_sizes: TensorLike
) -> tf.Tensor:
    """Shape [2 * dim + 1, dim] Tensor of points required for central difference

    For `i` in `range(dim)` this functions returns `points` s.t.:

    points[i]       = position + step[i]
    points[i + dim] = position - step[i]

    and in the last index:

    points[2 * dim] = position

    where `step` is a tensor of shape `[dim]` with a single non-zero element in index
    `i` with value `step_sizes[i]`.
    """

    dim = tf.shape(position)[0]

    return tf.tensor_scatter_nd_add(
        tensor=tf.tile(position[tf.newaxis, ...], [2 * dim + 1, 1]),
        indices=tf.stack([tf.range(2 * dim), tf.tile(tf.range(dim), [2])], axis=1),
        updates=tf.concat([step_sizes, -step_sizes], axis=0),
    )


def value_and_forward_difference(
    objective_fn: Callable,
    position: TensorLike,
    step_sizes: Optional[TensorLike] = None,
) -> tuple[tf.Tensor, tf.Tensor]:
    """Tuple of scalar value and tensor of forward difference gradient approximation

    The forward difference calculation is `(f(x + h) - f(x)) / h`.

    If the argument `step_sizes` is `None` then the function `step_sizes_one_sided` is
    used.
    """

    if step_sizes is None:
        step_sizes = step_sizes_one_sided(position)

    x = evaluation_points_one_sided(position, step_sizes, tf.tensor_scatter_nd_add)
    fx = objective_fn(x)
    value = fx[-1]
    forward_difference = (fx[:-1] - value) / step_sizes

    return value, forward_difference


def value_and_backward_difference(
    objective_fn: Callable,
    position: TensorLike,
    step_sizes: Optional[TensorLike] = None,
) -> tuple[tf.Tensor, tf.Tensor]:
    """Tuple of scalar value and tensor of backward difference gradient approximation

    The backward difference calculation is `(f(x) - f(x - h)) / h`.

    If the argument `step_sizes` is `None` then the function `step_sizes_one_sided` is
    used.
    """

    if step_sizes is None:
        step_sizes = step_sizes_one_sided(position)

    x = evaluation_points_one_sided(position, step_sizes, tf.tensor_scatter_nd_sub)
    fx = objective_fn(x)
    value = fx[-1]
    backward_difference = (value - fx[:-1]) / step_sizes

    return value, backward_difference


def value_and_central_difference(
    objective_fn: Callable,
    position: TensorLike,
    step_sizes: Optional[TensorLike] = None,
) -> tuple[tf.Tensor, tf.Tensor]:

    """Tuple of scalar value and tensor of central difference gradient approximation

    The central difference calculation is `(f(x + h) - f(x - h)) / (2 * h)`.

    If the argument `step_sizes` is `None` then the function `step_sizes_central` is
    used.
    """

    if step_sizes is None:
        step_sizes = step_sizes_central(position)

    x = evaluation_points_central(position, step_sizes)
    fx = objective_fn(x)
    value = fx[-1]
    dim = tf.shape(position)[0]
    central_difference = (fx[:dim] - fx[dim:-1]) / (2.0 * step_sizes)

    return value, central_difference
