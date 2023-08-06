from os.path import dirname, join, realpath

import matplotlib.pyplot as plt

from .colormap import *
from .distributions import *
from .utils import *

STYLE_DIR = realpath(join(dirname(__file__), 'styles'))
plt.style.use(join(STYLE_DIR, 'prettyplot.mplstyle'))

del plt, dirname, join, realpath
