import warnings
# This will omit annoying FutureWarnings by JAX and RutimeWarnings caused by
# estimates being clipped at bounds.
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)


from jax.config import config
config.update("jax_enable_x64", True)


from .models import ModelMixture, ModelLine, ModelMixtures, ModelWindow
from . import bridge_mixalime
from .utils import run
from gmpy2 import get_context
from mpmath import mp

_precision = 1024
get_context().precision = _precision
mp.prec = _precision


__version__ = "0.71"