"""Latent state visual stuff"""

import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tensorflow.types.experimental import TensorLike
from tensorflow_probability import bijectors as tfb


def time_series_plot(
    state_names: list[str],
    predicted_means: TensorLike,
    predicted_cov_diags: TensorLike,
    name: str = None,
    regex: str = None,
    num_std_errors: float = 2,
    bijector: tfb.Bijector = tfb.Identity(),
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Time series plots of predicted latent states"""

    if (name is None) == (regex is None):
        raise ValueError("Need to specify one of `name` and `regex`")

    if name is not None:
        indexes = np.where(np.array(state_names) == name)[0]

    if regex is not None:
        indexes = np.array(
            [i for i, x in enumerate(state_names) if re.search(regex, x)]
        )

    if indexes.shape[0] > 1:
        layout = [(indexes.shape[0] + 1) // 2, 2]
    else:
        layout = [1]

    mean = predicted_means.numpy()[:, indexes]
    std_error = np.sqrt(predicted_cov_diags)[:, indexes]
    names = np.array(state_names)[indexes]

    # assume Gaussian here
    median = bijector(mean).numpy()
    lower = bijector(mean - num_std_errors * std_error).numpy()
    upper = bijector(mean + num_std_errors * std_error).numpy()

    fig, axs = plt.subplots(*layout, **kwargs)

    axs = np.reshape(axs, [-1])

    timestep = np.arange(np.shape(predicted_means)[0])

    for ax, y, l, u, name in zip(axs, median.T, lower.T, upper.T, names):
        ax.plot(timestep, y)
        ax.fill_between(timestep, l, u, alpha=0.5)
        ax.set_title(name)
        ax.grid()

    if indexes.shape[0] > 1 and indexes.shape[0] % 2 == 1:
        fig.delaxes(ax=axs[-1])

    fig.add_subplot(111, frameon=False)
    fig.tight_layout()

    plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
    plt.xlabel("timestep")
    plt.ylabel(f"predicted latent state median $\\pm$ {num_std_errors} std. errors")

    return fig, axs


def to_dataframe(
    state_names: list[str], predicted_means: TensorLike, predicted_cov_diags: TensorLike
) -> pd.DataFrame:
    """pandas dataframe with the predicted latent state information"""

    num_timesteps = np.shape(predicted_means)[0]
    num_states = len(state_names)
    timestep = np.arange(num_timesteps, dtype=np.int32)

    df = pd.DataFrame(
        {
            "state": np.tile(state_names, num_timesteps),
            "timestep": np.repeat(timestep, num_states),
            "predicted_mean": np.reshape(predicted_means, [-1]),
            "predicted_cov_diag": np.reshape(predicted_cov_diags, [-1]),
        }
    )

    return df
