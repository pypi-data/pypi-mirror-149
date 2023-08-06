import matplotlib as mpl
import numpy as np

__all__ = ['make_cmap']


def make_cmap(
    colors: list,
    position: list = None,
    bit: bool = False,
    cmap_name: str = 'my_colormap',
):
    """Make a new color map based on the provided colors.

    @param colors : list
        values may either be in 8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default)
    @param position: list
        colors order
    @param bit: boolean
        Whether to use 8-bit or arithmetic (default)

    @return: Matplotlib Colormap

    """
    bit_rgb = np.linspace(0, 1, 256)
    if position is None:
        position = np.linspace(0, 1, len(colors))
    else:
        assert len(position) == len(colors), 'must be the same as colors'
        assert (position[0] == 0) and (
            position[-1] == 1
        ), 'position must start with 0 and end with 1'
    if bit:
        colors = [
            (bit_rgb[color[0]], bit_rgb[color[1]], bit_rgb[color[2]])
            for color in colors
        ]

    cdict = {'red': [], 'green': [], 'blue': []}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap(cmap_name, cdict, 256)
    return cmap


_categorical_lut = [
    (100, 143, 255),
    (120, 94, 240),
    (220, 38, 127),
    (254, 97, 0),
    (255, 176, 0),
]

_pantone_year = [
    (155, 183, 212),
    (199, 67, 117),
    (191, 25, 50),
    (123, 196, 196),
    (226, 88, 62),
    (83, 176, 174),
    (222, 205, 190),
    (155, 27, 48),
    (90, 91, 159),
    (240, 192, 90),
    (69, 181, 170),
    (217, 79, 112),
    (221, 65, 36),
    (0, 148, 115),
    (177, 99, 163),
    (149, 82, 81),
    (247, 202, 201),
    (146, 168, 209),
    (136, 176, 75),
    (95, 75, 139),
    (255, 111, 97),
    (15, 76, 129),
    (147, 149, 151),
    (245, 223, 77),
    (102, 103, 171),
]

_cold2hot_lut = [(29, 189, 230), (241, 81, 94)]

_lut_dict = dict(
    categorical=_categorical_lut,
    cold2hot=_cold2hot_lut,
    pantoneyear=_pantone_year,
)

for _name, _lut in _lut_dict.items():

    _cmap = make_cmap(_lut, bit=True, cmap_name=_name)
    locals()[_name] = _cmap

    _cmap_r = make_cmap(_lut[::-1], bit=True, cmap_name=_name + '_r')
    locals()[_name + '_r'] = _cmap_r

    mpl.cm.register_cmap(_name, _cmap)
    mpl.cm.register_cmap(_name + '_r', _cmap_r)

del mpl
