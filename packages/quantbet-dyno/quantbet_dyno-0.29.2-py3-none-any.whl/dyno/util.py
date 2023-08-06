"""Utilities that don't belong anywhere else"""

import inspect
import sys

from typing import Any

import numpy as np
import tensorflow as tf

from tensorflow import linalg as tfl
from tensorflow.types.experimental import TensorLike
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import prefer_static as ps
from tensorflow_probability.python.sts.internal import util as sts_util


def module_classes(module: str) -> list[Any]:
    """List all the classes in the module by string"""

    return inspect.getmembers(sys.modules[module], inspect.isclass)


def pad_leading_dimension(tensor: TensorLike, size: TensorLike):
    """pad tensor with `np.nan`"""

    paddings = tf.scatter_nd(
        indices=[[0, 1]],
        updates=[size - ps.shape(tensor)[0]],
        shape=[tf.rank(tensor), 2],
    )

    return tf.pad(
        tensor=tensor, paddings=paddings, mode="CONSTANT", constant_values=np.nan
    )


def remove_leading_padding(tensor: TensorLike) -> tf.Tensor:
    """remove `np.nan` padding"""

    mask = ~tf.reduce_all(tf.math.is_nan(tensor), axis=tf.range(1, tf.rank(tensor)))

    return tf.boolean_mask(tensor=tensor, mask=mask, axis=0)


# NOTE: This is an almost copy-paste of the same function in
#       tensorflow_probability/python/sts/internal/util.py
#       However, we noticed that the `proto_data` messages
#       being created by TFP when it creates its graph were
#       growing insanely long. These messages are massively
#       reduced in size by simply assigning a `name` attribute
#       to the variables in this function for some reason.
def factored_joint_mvn(distributions):
    """Combine MultivariateNormals into a factored joint distribution.

     Given a list of multivariate normal distributions
     `dist[i] = Normal(loc[i], scale[i])`, construct the joint
     distribution given by concatenating independent samples from these
     distributions. This is multivariate normal with mean vector given by the
     concatenation of the component mean vectors, and block-diagonal covariance
     matrix in which the blocks are the component covariances.

     Note that for computational efficiency, multivariate normals are represented
     by a 'scale' (factored covariance) linear operator rather than the full
     covariance matrix.

    Args:
      distributions: Python `iterable` of MultivariateNormal distribution
        instances (e.g., `tfd.MultivariateNormalDiag`,
        `tfd.MultivariateNormalTriL`, etc.). These must be broadcastable to a
        consistent batch shape, but may have different event shapes
        (i.e., defined over spaces of different dimension).

    Returns:
      joint_distribution: An instance of `tfd.MultivariateNormalLinearOperator`
        representing the joint distribution constructed by concatenating
        an independent sample from each input distributions.
    """

    with tf.name_scope("factored_joint_mvn"):

        # We explicitly broadcast the `locs` so that we can concatenate them.
        # We don't have direct numerical access to the `scales`, which are arbitrary
        # linear operators, but `LinearOperatorBlockDiag` appears to do the right
        # thing without further intervention.
        dtype = tf.debugging.assert_same_float_dtype(distributions)
        broadcast_ones = tf.ones(
            sts_util.broadcast_batch_shape(distributions), dtype=dtype
        )[..., tf.newaxis]
        return tfd.MultivariateNormalLinearOperator(
            loc=tf.concat(
                [mvn.mean() * broadcast_ones for mvn in distributions],
                axis=-1,
            ),
            scale=tfl.LinearOperatorBlockDiag(
                [mvn.scale for mvn in distributions],
                is_square=True,
                name="lop",  # <-- hugely reduces protobuf message sizes
            ),
            name="mvn",
        )
