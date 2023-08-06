"""Model parameters definition"""

import itertools as it

from dataclasses import dataclass
from typing import Optional
from typing import Union

import tensorflow as tf

from tensorflow.types.experimental import TensorLike
from tensorflow_probability import bijectors as tfb
from tensorflow_probability import distributions as tfd
from tensorflow_probability.python.internal import dtype_util

# TODO(jeff): do we need to differentiate between the "total" number of parameters (the
#             sum of `event_shape.num_elements()` for each parameter) and the number of
#             parameters?


def _transform_reshape_split_bijector(joint_dist, bijectors):

    unconstrained_shapes = [
        x.inverse_event_shape(y)
        for x, y in zip(bijectors, tf.nest.flatten(joint_dist.event_shape))
    ]

    # this reshaping is required as as split can produce a tensor of shape [1]
    # when the distribution event shape is []
    reshapers = [
        tfb.Reshape(event_shape_out=x, event_shape_in=[x.num_elements()])
        for x in unconstrained_shapes
    ]

    size_splits = [x.num_elements() for x in unconstrained_shapes]

    return tfb.Chain(
        [
            tfb.JointMap(bijectors=bijectors),
            tfb.JointMap(bijectors=reshapers),
            tfb.Split(num_or_size_splits=size_splits),
        ]
    )


@dataclass
class Parameter:
    """Structure to hold model parameter attributes.

    Since parameters often work on some subset of the real numbers, e.g. [0, +inf) for
    scale type parameters, we use a so-called "constraining bijector" to map from the
    real numbers to the parameter domain. This is since most optimisation algorithms
    work on the real numbers (which we refer to as the "unconstrained" domain). The
    bijector `forward` method constrains the parameter, e.g. maps from the real numbers
    to the parameter domain, and the `inverse` method unconstrains the parameter. Both
    the `inverse` and `forward` methods are used internally in `dyno` when fitting.

    If `constraining_bijector` is not specified, a default one can be taken from the
    `prior`, for example:

    ``` python
    dist = tfd.Exponential(rate=1.0)
    dist.experimental_default_event_space_bijector()
    # ===> <tensorflow_probability.python.bijectors.softplus.Softplus object at 0x7f33f3cfef70>
    ````

    """

    name: str
    prior: tfd.Distribution
    initial_position: Union[tf.Tensor, float]
    constraining_bijector: Optional[tfb.Bijector] = None


class ModelParameters:
    """Hold a list of `Parameter` instances.

    The main use of the class is to piece together individual parameters into a tensor
    which can be passed to optimisation algorithms. This tensor is referred to as the
    "unconstrained" values of the parameters.

    """

    def __init__(self, parameters: list[Parameter]):

        dtype = dtype_util.common_dtype(
            [p.prior for p in parameters] + [p.initial_position for p in parameters],
            dtype_hint=tf.float32,
        )

        initial_position = [
            tf.convert_to_tensor(p.initial_position, dtype=dtype) for p in parameters
        ]

        for p, ip in zip(parameters, initial_position):
            if p.prior.event_shape != ip.shape:
                raise ValueError(
                    f"prior: {p.prior} not consistent with initial position: {ip}"
                )

        self._initial_position = initial_position
        self._parameters = parameters
        self._dtype = dtype

        bijectors = [
            p.prior.experimental_default_event_space_bijector()
            if p.constraining_bijector is None
            else p.constraining_bijector
            for p in parameters
        ]

        self._joint_dist = tfd.JointDistributionSequential(
            [p.prior for p in parameters]
        )

        self._joint_bijector = _transform_reshape_split_bijector(
            self._joint_dist, bijectors
        )

    def constrain(self, position: TensorLike) -> list[tf.Tensor]:
        return self.joint_bijector.forward(position)

    def unconstrain(self, position: list[TensorLike]) -> tf.Tensor:
        return self.joint_bijector.inverse(position)

    def log_prob(self, position: list[TensorLike]):
        return self.joint_distribution.log_prob(position)

    def sample(self, sample_shape=()):
        return self.joint_distribution.sample(sample_shape)

    @property
    def initial_position(self) -> list[tf.Tensor]:
        return self._initial_position

    @property
    def unconstrained_initial_position(self) -> tf.Tensor:
        return self.unconstrain(self.initial_position)

    @property
    def parameter_names(self) -> list[str]:
        return [p.name for p in self.parameters]

    @property
    def element_names(self) -> list[str]:
        names = []
        for p in self.parameters:
            event_shape = p.prior.event_shape
            name = p.name
            if event_shape == []:
                names.append(name)
            else:
                for element in it.product(*[range(shape) for shape in event_shape]):
                    element_str = ",".join([str(e) for e in element])
                    names.append(f"{name}[{element_str}]")
        return names

    @property
    def joint_distribution(self) -> tfd.JointDistribution:
        return self._joint_dist

    @property
    def joint_bijector(self) -> tfb.Bijector:
        return self._joint_bijector

    @property
    def parameters(self) -> list[Parameter]:
        return self._parameters

    @property
    def num_parameters(self) -> int:
        return len(self.parameters)

    @property
    def dtype(self) -> tf.DType:
        return self._dtype

    @property
    def num_elements(self) -> list[int]:
        return [p.prior.event_shape.num_elements() for p in self.parameters]

    @property
    def num_unconstrained_elements(self) -> int:
        return self.unconstrain(self.initial_position).shape.num_elements()
