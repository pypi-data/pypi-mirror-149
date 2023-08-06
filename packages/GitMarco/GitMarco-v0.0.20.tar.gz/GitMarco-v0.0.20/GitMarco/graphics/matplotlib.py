import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


def validation_plot(
        true: np.ndarray,
        pred: np.ndarray,
        size: tuple = (6, 6),
        title: str = '',
        show: bool = False,
        xlabel: str = 'x',
        ylabel: str = 'y',
        marker_color: str = 'b',
        edge_color: str = 'k',
        line_color: str = 'k',
):
    true = true.reshape(-1, 1) if isinstance(true, np.ndarray) else None
    pred = pred.reshape(-1, 1) if isinstance(pred, np.ndarray) else None
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=size)
    ax.scatter(true, pred, c=marker_color, edgecolor=edge_color)
    min_ = min((min(true), min(pred)))
    max_ = max((max(true), max(pred)))
    plt.plot([min_, max_], [min_, max_], '-.', c=line_color, linewidth=0.5)
    ax.set_title(f'{title} - R2: {r2_score(true, pred)}')
    ax.set_xlim(min_, max_)
    ax.set_ylim(min_, max_)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid('both')
    plt.show() if show else None
    return fig, ax


def plot_2d(
        x,
        y,
        label: str or list = '',
        size: tuple = (6, 6),
        title: str = '',
        show: bool = False,
        xlabel: str = 'x',
        ylabel: str = 'y',
        line_color: str = 'k',
        line_width: int = 1,
        xlim: tuple = None,
        ylim: tuple = None,

):
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=size)

    if isinstance(x, list) and isinstance(y, list) and isinstance(label, list):
        for i in range(len(x)):
            plt.plot(x[i],
                     y[i],
                     # line_color=line_color,
                     linewidth=line_width,
                     label=label[i]
                     )
    else:
        plt.plot(x,
                 y,
                 c=line_color,
                 linewidth=line_width,
                 label=label
                 )

    plt.legend()
    ax.set_title(f'{title}')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show() if show else None
    return fig, ax


def scatter_2d(
        x,
        y,
        label: str or list = '',
        size: tuple = (6, 6),
        title: str = '',
        show: bool = False,
        xlabel: str = 'x',
        ylabel: str = 'y',
        marker: str = '^',
        marker_color: str = 'b',
        edge_color: str = 'k',
        xlim: tuple = None,
        ylim: tuple = None,

):
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots(figsize=size)

    if isinstance(x, list) and isinstance(y, list) and isinstance(label, list):
        for i in range(len(x)):
            plt.scatter(x[i],
                        y[i],
                        # line_color=line_color,
                        edgecolor=edge_color,
                        marker=marker,
                        label=label[i]
                        )
    else:
        plt.scatter(x,
                    y,
                    c=marker_color,
                    marker=marker,
                    edgecolor=edge_color,
                    label=label,
                    )

    plt.legend()
    ax.set_title(f'{title}')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show() if show else None
    return fig, ax


def circle(
        n: int = 400,
        r: float = 0.2,
        c: tuple = (0.5, 0.),
        show: bool = False,
) -> np.ndarray:
    theta = np.linspace(0, 2 * np.pi, n)
    radius = r
    # Generating x and y data
    x = radius * np.cos(theta) + c[0]
    y = radius * np.sin(theta) + c[1]

    if show:
        plt.plot(x, y)
        plt.axis('equal')
        plt.title('Circle')
        plt.show()

    return np.expand_dims(np.stack((x, y,), axis=1), axis=0)
