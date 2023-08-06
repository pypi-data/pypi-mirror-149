import numpy as np

__all__ = ['hex2rgb', 'rgb2hex']


def hex2rgb(hexcode: str) -> tuple:
    return tuple(int(hexcode.lstrip('#')[i : i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb: tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format(*rgb).upper()


def _get_aspect(ax):
    figW, figH = ax.get_figure().get_size_inches()
    _, _, w, h = ax.get_position().bounds
    disp_ratio = (figH * h) / (figW * w)
    data_ratio = np.diff(ax.get_ylim()) / np.diff(ax.get_xlim())

    return disp_ratio / data_ratio


def _check_argument(param, options, value):
    """Raise if value for param is not in options."""
    if value not in options:
        raise ValueError(
            f'`{param}` must be one of {options}, but {repr(value)} was passed.'
        )
