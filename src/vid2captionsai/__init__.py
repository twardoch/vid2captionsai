import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "unknown"
finally:
    del version, PackageNotFoundError

# Import main class for easy access
from .vid2captionsai import PrepAudioVideo

__all__ = ["PrepAudioVideo", "__version__"]
