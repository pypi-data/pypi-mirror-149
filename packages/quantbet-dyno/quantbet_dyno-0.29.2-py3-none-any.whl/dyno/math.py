"""Math functions not found elsewhere"""

import numpy as np
import tensorflow as tf

from tensorflow.types.experimental import TensorLike
from tensorflow_probability.python.internal import prefer_static as ps


def _b_spline_weight(x, index, augmented_knots, degree):
    lower = augmented_knots[index]
    upper = augmented_knots[index + degree + 1]
    weight = (x - lower) / (upper - lower)
    return tf.where(tf.equal(upper, lower), tf.zeros_like(weight), weight)


def _b_spline_constant(x, index, augmented_knots):
    within_knots = (augmented_knots[index] <= x) & (x < augmented_knots[index + 1])
    return tf.cast(within_knots, x.dtype)


def _b_spline_linear(x, index, augmented_knots):
    weight0 = _b_spline_weight(x, index, augmented_knots, degree=0)
    weight1 = 1.0 - _b_spline_weight(x, index + 1, augmented_knots, degree=0)
    basis0 = _b_spline_constant(x, index, augmented_knots)
    basis1 = _b_spline_constant(x, index + 1, augmented_knots)
    return weight0 * basis0 + weight1 * basis1


def _b_spline_quadratic(x, index, augmented_knots):
    weight0 = _b_spline_weight(x, index, augmented_knots, degree=1)
    weight1 = 1.0 - _b_spline_weight(x, index + 1, augmented_knots, degree=1)
    basis0 = _b_spline_linear(x, index, augmented_knots)
    basis1 = _b_spline_linear(x, index + 1, augmented_knots)
    return weight0 * basis0 + weight1 * basis1


def _b_spline_cubic(x, index, augmented_knots):
    weight0 = _b_spline_weight(x, index, augmented_knots, degree=2)
    weight1 = 1.0 - _b_spline_weight(x, index + 1, augmented_knots, degree=2)
    basis0 = _b_spline_quadratic(x, index, augmented_knots)
    basis1 = _b_spline_quadratic(x, index + 1, augmented_knots)
    return weight0 * basis0 + weight1 * basis1


def _b_spline_quartic(x, index, augmented_knots):
    weight0 = _b_spline_weight(x, index, augmented_knots, degree=3)
    weight1 = 1.0 - _b_spline_weight(x, index + 1, augmented_knots, degree=3)
    basis0 = _b_spline_cubic(x, index, augmented_knots)
    basis1 = _b_spline_cubic(x, index + 1, augmented_knots)
    return weight0 * basis0 + weight1 * basis1


_B_SPLINE_BASIS_FUNCTIONS = [
    _b_spline_constant,
    _b_spline_linear,
    _b_spline_quadratic,
    _b_spline_cubic,
    _b_spline_quartic,
]


class BSpline:
    """Class for generating B-spline basis matrices"""

    _MAX_DEGREE = 4

    def __init__(self, degree: int, knots: TensorLike, intercept: bool):
        """Initialise a `BSpline` object"""

        if not 0 <= degree <= self._MAX_DEGREE:
            raise ValueError(f"input `degree` should be >= 0 and <= {self._MAX_DEGREE}")

        knots = tf.convert_to_tensor(knots)

        ascending_knots_assertion = tf.assert_greater(
            knots[..., 1:],
            knots[..., :-1],
            message="input `knots` must be strictly increasing.",
        )

        with tf.control_dependencies([ascending_knots_assertion]):
            self._knots = knots

        dtype = knots.dtype

        broadcast_degree = tf.concat([ps.shape(knots)[:-1], [degree]], axis=0)
        eps = np.finfo(dtype.as_numpy_dtype).eps
        augmented_knots = tf.concat(
            [
                tf.broadcast_to(knots[..., 0], broadcast_degree),
                knots,
                tf.broadcast_to(knots[..., -1], broadcast_degree) + eps,
            ],
            axis=0,
        )

        self._intercept = intercept
        self._dtype = dtype
        self._df = ps.shape(knots)[-1] + degree - 1
        self._degree = degree
        self._augmented_knots = augmented_knots
        self._basis_fn = _B_SPLINE_BASIS_FUNCTIONS[degree]

    @property
    def intercept(self) -> bool:
        """Boolean indicator for if the basis includes the first column"""
        return self._intercept

    @property
    def dtype(self) -> tf.DType:
        """The `DType` of `tf.Tensor`s handled by this spline"""
        return self._dtype

    @property
    def degree(self) -> int:
        """Degree of the piecewise polynomial"""
        return self._degree

    @property
    def knots(self) -> tf.Tensor:
        """The (ascending) breakpoints which define the spline"""
        return self._knots

    @property
    def df(self) -> int:
        """The spline degrees of freedom (number of columns in the basis matrix)"""
        return self._df - (not self.intercept)

    def basis(self, x) -> tf.Tensor:
        """The (possible batched) basis matrix"""
        x = tf.convert_to_tensor(x, dtype_hint=self.dtype)
        basis_vectors = [
            self._basis_fn(x, index + (not self.intercept), self._augmented_knots)
            for index in range(self.df)
        ]
        return tf.stack(basis_vectors, axis=-1)


def logit(x: TensorLike) -> tf.Tensor:
    """The logit function log(p / (1 - p))"""
    return -tf.math.log(tf.math.reciprocal(x) - 1.0)
