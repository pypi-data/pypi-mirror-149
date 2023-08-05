from .main import *
from .para import *
from .tensor_scaling import rescale_lambda_centerized_workhorse
from .tensor_scaling import rescale_lambda_centerized

from .hdf5_io import *
from .coil import *
from .exp import *
from .util import *
from .freesurfer import *
from .roi import *
from .subject import *
from .postproc import *
from .simnibs import *
import pynibs.models
from .exp import *
from .opt import *

try:
    from .pckg import libeep
except (ImportError, SyntaxError):
    # print("libeep not found. visor import will not work.")
    pass
try:
    from paraview.simple import *
except ImportError:
    # print("Paraview not installed. Plot functionalities will not work.")
    pass