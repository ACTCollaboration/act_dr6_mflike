from .act_dr6_mflike import ACTDR6MFLike
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("act_dr6_mflike")
except PackageNotFoundError:
    # package is not installed
    pass
