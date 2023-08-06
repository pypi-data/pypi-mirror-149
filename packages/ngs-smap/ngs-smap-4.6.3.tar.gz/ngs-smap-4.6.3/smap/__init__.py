from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution('ngs-smap').version
except DistributionNotFound:
    # package is not installed
    pass
__all__ = ["__version__"]
