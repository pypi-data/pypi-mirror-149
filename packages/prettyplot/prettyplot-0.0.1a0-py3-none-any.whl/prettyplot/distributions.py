import copy

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform
from sklearn.model_selection import KFold, RandomizedSearchCV
from sklearn.neighbors import KernelDensity

from .utils import _check_argument, _get_aspect

__all__ = ['raincloud']


class _CategoricalData(object):
    def set_variables(self, data, pos, label):
        assert (
            data is not None
        ), f'Expected 2D array, got scalar array instead:\narray={data}.\n'
        if hasattr(data, 'ndim'):
            if data.ndim == 0:
                raise ValueError(
                    f'Expected 2D array, got scalar array instead:\narray={data}.\n'
                )

            if data.ndim == 1:
                raise ValueError(
                    f'Expected 2D array, got 1D array instead:\narray={data}.\n'
                )

            data = data.tolist()

        else:
            if not all(
                map(
                    lambda value: isinstance(value, (list, tuple, np.ndarray)),
                    data,
                )
            ):
                raise ValueError(
                    f'Expected 2D array, got scalar multidimensional array instead:\narray={data}.\n'
                )

        self.data = data
        for num in range(len(self.data)):
            self.data[num] = np.array(self.data[num])

        if pos is not None:
            if hasattr(pos, 'ndim'):
                if pos.ndim == 0:
                    raise ValueError(
                        f'Expected 1D array, got scalar array instead:\narray={pos}.\n'
                    )

                if pos.ndim > 1:
                    raise ValueError(
                        f'Expected 1D array, got multidimensional array instead:\narray={pos}.\n'
                    )
                pos = pos.tolist()

            if not all(map(lambda value: isinstance(value, int), pos)):
                raise ValueError(
                    f'Expected 1D numeric type array, got non-numeric type instead:\narray={pos}.\n'
                )

            if len(pos) != len(self.data):
                raise ValueError(
                    'Positional array have more elements than groupes in Data array.'
                )
            self.pos = pos

        else:
            self.pos = list(range(len(self.data)))

        if label is not None:
            if len(label) != len(self.data):
                raise ValueError(
                    'Positional array have more elements than groupes in Data array.'
                )

            if not all(
                map(
                    lambda value: not isinstance(
                        value, (tuple, list, np.ndarray, set)
                    ),
                    label,
                )
            ):
                raise ValueError(
                    f'Expected 1D categorical type array, got non-categorical type instead:\narray={pos}.\n'
                )
            self.label = np.asarray(label)

        else:
            self.label = np.asarray(self.pos)


class _RainCloudPlotter(_CategoricalData):
    def __init__(
        self, data, pos, label, cmap, width, sjitter, kjitter, side, n_iter
    ):
        self.set_variables(data, pos, label)
        self.cmap = cmap
        self.width = width
        self.sjitter = sjitter
        self.kjitter = kjitter
        self.side = side
        self.n_iter = n_iter
        self.xds = []
        self.kdes = []

    def draw_boxplot(self, ax, kws):
        props = {}
        for obj in ['box', 'whisker', 'cap', 'median', 'flier']:
            props[obj] = kws.pop(obj + 'props', {})

        for group_pos, group_data in zip(self.pos, self.data):
            if group_data.size == 0:
                continue

            box_data = np.asarray(group_data, float)

            artist_dict = ax.boxplot(
                box_data,
                patch_artist=True,
                positions=[group_pos],
                widths=self.width,
                **kws,
            )

            x, y = artist_dict['medians'][0].get_data()
            ax.add_artist(
                mpl.patches.Ellipse(
                    (x.mean(), y.mean()),
                    (x[1] - x[0]) / 2,
                    (x[1] - x[0]) / 2 * 1 / _get_aspect(ax),
                    color='w',
                    zorder=kws['zorder'] + 1,
                )
            )
            self.restyle_boxplot(artist_dict, props)

    def restyle_boxplot(self, artist_dict, props):
        """Take a drawn matplotlib boxplot and make it look nice."""
        for box in artist_dict['boxes']:
            box.update(dict(facecolor='k', linestyle='None'))
            box.update(props['box'])

        for whisk in artist_dict['whiskers']:
            whisk.update(props['whisker'])

        for cap in artist_dict['caps']:
            cap.update(dict(color='None'))
            cap.update(props['cap'])

        for med in artist_dict['medians']:
            med.set(color='None')

        for fly in artist_dict['fliers']:
            fly.update(dict(markerfacecolor='None', markeredgecolor='None'))
            fly.update(props['flier'])

    def draw_scatter(self, ax, kws):
        for group_pos, group_data in zip(self.pos, self.data):
            if self.side == 'invert':
                ax.scatter(
                    group_pos
                    + np.random.uniform(0, -self.sjitter, len(group_data)),
                    group_data,
                    color=self.cmap(
                        (self.pos.index(group_pos) + 1) / (len(self.pos) + 1)
                    ),
                    **kws,
                )
            else:
                ax.scatter(
                    group_pos
                    + np.random.uniform(0, self.sjitter, len(group_data)),
                    group_data,
                    color=self.cmap(
                        (self.pos.index(group_pos) + 1) / (len(self.pos) + 1)
                    ),
                    **kws,
                )

    def fit_kde(self):
        for group_data in self.data:
            grid = RandomizedSearchCV(
                KernelDensity(kernel='gaussian'),
                {'bandwidth': uniform(loc=0, scale=1e3)},
                n_iter=self.n_iter,
                cv=KFold(
                    n_splits=5 if len(group_data) >= 100 else len(group_data)
                ),
                n_jobs=-1,
            )
            grid.fit(group_data[:, None])

            self.xds.append(
                np.linspace(group_data.min(), group_data.max(), 1000)
            )
            self.kdes.append(
                np.exp(
                    grid.best_estimator_.score_samples(self.xds[-1][:, None])
                )
            )

    def draw_fillbtw(self, ax, kws):
        self.fit_kde()
        for group_pos, xd, kde in zip(self.pos, self.xds, self.kdes):
            if self.side == 'invert':
                ax.fill_betweenx(
                    xd,
                    group_pos + kde * self.kjitter,
                    group_pos,
                    color=self.cmap(
                        (self.pos.index(group_pos) + 1) / (len(self.pos) + 1)
                    ),
                    **kws,
                )

            else:
                ax.fill_betweenx(
                    xd,
                    group_pos - kde * self.kjitter,
                    group_pos,
                    color=self.cmap(
                        (self.pos.index(group_pos) + 1) / (len(self.pos) + 1)
                    ),
                    **kws,
                )

    def plot(self, ax, scatter_kws, boxplot_kws, fillbtw_kws):
        for key, value in {'alpha': 0.3, 'zorder': 1}.items():
            scatter_kws.setdefault(key, value)
            fillbtw_kws.setdefault(key, value)

        scatter_kws.setdefault('s', 3)
        boxplot_kws.setdefault('zorder', 2)
        self.draw_scatter(ax, scatter_kws)
        self.draw_fillbtw(ax, fillbtw_kws)
        self.draw_boxplot(ax, boxplot_kws)

        ax.set_xlim(-0.5, max(self.pos) + 0.5)
        ax.set_xticks(self.pos)
        ax.set_xticklabels(self.label[self.pos])


def raincloud(
    *,
    data=None,
    pos=None,
    label=None,
    cmap='viridis',
    width: float = 0.05,
    sjitter: float = 0.3,
    kjitter: float = 1,
    ax=None,
    side: str = 'normal',
    n_iter: int = 1000,
    scatter_kws=None,
    boxplot_kws=None,
    fillbtw_kws=None,
):
    # -- Input Checking
    _check_argument('side', ['normal', 'invert'], side)

    # -- Initializing
    scatter_kws = {} if scatter_kws is None else copy.copy(scatter_kws)
    boxplot_kws = {} if boxplot_kws is None else copy.copy(boxplot_kws)
    fillbtw_kws = {} if fillbtw_kws is None else copy.copy(fillbtw_kws)
    cmap = plt.get_cmap(cmap) if isinstance(cmap, str) else cmap

    # -- Plotting
    if ax is None:
        ax = plt.gca()

    plotter = _RainCloudPlotter(
        data, pos, label, cmap, width, sjitter, kjitter, side, n_iter
    )

    plotter.plot(ax, scatter_kws, boxplot_kws, fillbtw_kws)

    return ax
