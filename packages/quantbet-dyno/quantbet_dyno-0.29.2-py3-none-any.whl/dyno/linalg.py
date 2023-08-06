"""Linear algebra"""

import functools

from typing import Callable

import numpy as np
import tensorflow as tf

from tensorflow import linalg as tfl
from tensorflow.types.experimental import TensorLike
from tensorflow_probability.python.internal import dtype_util
from tensorflow_probability.python.internal import prefer_static as ps


def mvn_tril_2d(
    scale1: TensorLike, scale2: TensorLike, correlation: TensorLike
) -> tfl.LinearOperator:
    """LinearOperatorLowerTriangular for cholesky factor of 2x2 covariance matrix"""

    dtype = dtype_util.common_dtype([scale1, scale2, correlation], tf.float32)

    scale1 = tf.convert_to_tensor(scale1, dtype)
    scale2 = tf.convert_to_tensor(scale2, dtype)
    correlation = tf.convert_to_tensor(correlation, dtype)

    batch_shape = functools.reduce(
        ps.broadcast_shape, [ps.shape(scale1), ps.shape(scale2), ps.shape(correlation)]
    )

    scale1 = tf.broadcast_to(scale1, batch_shape)
    scale2 = tf.broadcast_to(scale2, batch_shape)
    correlation = tf.broadcast_to(correlation, batch_shape)

    flat_scale_tril = tf.stack(
        [
            scale1,
            tf.zeros(batch_shape, dtype),
            correlation * scale2,
            scale2 * tf.math.sqrt(1.0 - tf.square(correlation)),
        ],
        axis=-1,
    )

    scale_tril = tf.reshape(flat_scale_tril, tf.concat([batch_shape, [2, 2]], axis=0))

    return tfl.LinearOperatorLowerTriangular(scale_tril)


def symmetric_inv(symmetric_matrix: TensorLike) -> tf.Tensor:
    """Invert a symmetric matrix using a cholesky decomposition"""

    chol = tfl.cholesky(symmetric_matrix)
    dim = ps.shape(symmetric_matrix)[-1]
    eye = tf.eye(dim, dtype=chol.dtype)
    inv = tfl.cholesky_solve(chol, eye)

    return inv


def build_covariance_matrix(
    correlation_matrix: TensorLike, scale: TensorLike
) -> tf.Tensor:
    """Build a covariance matrix from correlation and scale"""

    scale_diag = tfl.LinearOperatorDiag(scale)

    return scale_diag @ correlation_matrix @ scale_diag


def decompose_covariance_matrix(
    covariance_matrix: TensorLike,
) -> tuple[tf.Tensor, tf.Tensor]:
    """Decompose a covariance matrix into (correlation_matrix, scale)"""

    scale = tf.math.sqrt(tfl.diag_part(covariance_matrix))

    precision_diag = tfl.LinearOperatorDiag(tf.math.reciprocal(scale))

    correlation_matrix = precision_diag @ covariance_matrix @ precision_diag

    return correlation_matrix, scale


def extract_block_diagonals_with_size(
    matrix: TensorLike, size: int, parallel_iterations: int = 10
) -> tf.Tensor:
    """Extract same sized matrices from the diagonal, `size` should be python"""

    num_rows = tf.shape(matrix)[0]

    def not_empty_fn():
        num_blocks = num_rows // size

        def cond(block, _):
            return block < num_blocks

        def body(block, ta):
            i = block * size
            j = i + size
            return block + 1, ta.write(block, matrix[i:j, i:j])

        ta = tf.TensorArray(
            dtype=matrix.dtype,
            size=num_blocks,
            dynamic_size=False,
            infer_shape=True,
            element_shape=tf.TensorShape([size, size]),
        )

        init = [tf.constant(0, dtype=num_rows.dtype), ta]

        _, blocks = tf.while_loop(
            cond, body, init, parallel_iterations=parallel_iterations
        )

        return blocks.stack()

    def empty_fn():
        return tf.constant(np.empty([0, size, size], dtype=matrix.dtype.as_numpy_dtype))

    return tf.cond(tf.equal(num_rows, 0), empty_fn, not_empty_fn)


def interleave_matrix_columns(matrices: list[TensorLike]) -> tf.Tensor:
    """Combine matrix columns from a list of matrices"""

    # assume matrices are all the same shape
    shape = ps.shape(matrices[0])

    num_cols = shape[-1]
    num_rows = shape[-2]
    batch_shape = shape[:-2]

    column_shape = tf.concat([batch_shape, [num_rows * num_cols], [1]], axis=0)
    columns = [tf.reshape(x, column_shape) for x in matrices]
    combined_columns = tf.concat(columns, axis=-1)

    interleaved_shape = tf.concat(
        [batch_shape, [num_rows], [num_cols * len(matrices)]], axis=0
    )

    return tf.reshape(combined_columns, interleaved_shape)


def elementwise_diagonal_expand(matrix: TensorLike, size: int) -> tf.Tensor:
    """Each element in `matrix` becomes a block diagonal matrix with (static) `size`"""

    shape = matrix.shape

    if shape is None:
        raise ValueError("matrix shape must be known statically")

    if len(shape) > 2:
        raise ValueError("matrix batching not supported")

    ta = tf.TensorArray(
        dtype=matrix.dtype, size=shape[0], element_shape=tf.TensorShape([None, None])
    )

    def cond(i, *_):
        return i < shape[0]

    def body(i, ta):
        row_elements = tf.split(matrix[i], tf.fill([shape[1]], 1))
        diags = tf.concat(
            [tfl.diag(tf.fill([size], x[0])) for x in row_elements], axis=1
        )
        return i + 1, ta.write(i, diags)

    _, ta_ = tf.while_loop(cond=cond, body=body, loop_vars=[0, ta])

    return ta_.concat()


def _eager_value_and_hessian(fn, x, has_batch_dims):
    """value and gradient implementation compatible with eager"""

    with tf.GradientTape(persistent=True, watch_accessed_variables=False) as tape:
        tape.watch(x)
        value = fn(x)
        gradient = tape.gradient(value, x)

    if has_batch_dims:
        hessian = tape.batch_jacobian(gradient, x)
    else:
        hessian = tape.jacobian(gradient, x)

    return value, hessian


def _graph_value_and_hessian(fn, x, has_batch_dims):
    """more efficient value and gradient implementation for graph case"""

    value = fn(x)
    hessian = tf.hessians(ys=value, xs=x)[0]

    if has_batch_dims:
        hessian = tf.reduce_sum(hessian, axis=-2)

    return value, hessian


def value_and_hessian(
    fn: Callable, x: TensorLike, *args, **kwargs
) -> tuple[tf.Tensor, tf.Tensor]:
    """Like `tfp.math.value_and_gradient` but for hessians"""

    # TODO(jeff): keep track of
    # https://github.com/tensorflow/tensorflow/issues/29781#issuecomment-591023914

    x = tf.convert_to_tensor(x)

    batch_shape = x.shape[:-1]

    if batch_shape is None:
        raise ValueError("shape of `x` must be known statically")

    if batch_shape.ndims > 1:
        raise ValueError("only single batch dimension is currently supported")

    has_batch_dims = batch_shape.ndims > 0

    if tf.executing_eagerly():
        return _eager_value_and_hessian(fn=fn, x=x, has_batch_dims=has_batch_dims)

    return _graph_value_and_hessian(fn=fn, x=x, has_batch_dims=has_batch_dims)


def slice_symmetric_matrix(matrix: TensorLike, indices: TensorLike) -> tf.Tensor:
    """Slice a symmetric matrix into another symmetric matrix"""

    return slice_matrix(matrix, indices, indices)


def slice_matrix(
    matrix: TensorLike, row_indices: TensorLike, col_indices: TensorLike
) -> tf.Tensor:
    """Slice a matrix using row and column indices"""

    sliced_dim = tf.concat(
        [tf.shape(row_indices)[-1:], tf.shape(col_indices)[-1:]], axis=0
    )

    batch_shape = ps.shape(matrix)[:-2]
    batch_dims = ps.rank(matrix) - 2

    row_indices = tf.repeat(row_indices, sliced_dim[1])
    col_indices = tf.tile(col_indices, [sliced_dim[0]])

    matrix_indices = tf.stack([row_indices, col_indices], axis=-1)
    batched_matrix_indices_shape = tf.concat(
        [batch_shape, tf.shape(matrix_indices)], axis=0
    )
    batched_matrix_indices = tf.broadcast_to(
        matrix_indices, batched_matrix_indices_shape
    )

    batched_values = tf.gather_nd(matrix, batched_matrix_indices, batch_dims=batch_dims)

    return tf.reshape(batched_values, tf.concat([batch_shape, sliced_dim], axis=0))
