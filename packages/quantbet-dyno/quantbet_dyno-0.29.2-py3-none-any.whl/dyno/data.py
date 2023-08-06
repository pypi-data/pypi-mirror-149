"""Dynamic data"""

import tensorflow as tf

from tensorflow.types.experimental import TensorLike


def timestep_counts(timestep: TensorLike) -> tf.Tensor:
    """Count the number of entries for each possible timestep"""

    # scared this could be a bug source so check it
    assertion = tf.assert_equal(
        x=timestep[0],
        y=tf.constant(0, dtype=timestep.dtype),
        message="timestep should start with value 0",
    )

    with tf.control_dependencies([assertion]):
        return tf.math.bincount(timestep)


def ragged_timestep_data(x: TensorLike, counts: TensorLike) -> tf.RaggedTensor:
    """`tf.RaggedTensor` from x using timestep counts"""

    return tf.RaggedTensor.from_row_lengths(x, counts)
