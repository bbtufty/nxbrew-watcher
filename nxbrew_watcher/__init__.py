from importlib.metadata import version

# Get the version
__version__ = version(__name__)

from .watcher import NXBrewWatcher

__all__ = [
    "NXBrewWatcher",
]
