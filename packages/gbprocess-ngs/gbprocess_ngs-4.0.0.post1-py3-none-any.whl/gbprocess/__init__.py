from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("gbprocess-ngs").version
except DistributionNotFound:
    # package is not installed
    pass
__all__ = ["__version__"]
