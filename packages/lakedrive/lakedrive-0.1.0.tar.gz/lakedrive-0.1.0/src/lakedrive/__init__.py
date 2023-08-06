__version__ = "0.1.0"
import logging
from .core.sync import rsync_paths
from .cli import main  # noqa: F401

__all__ = ["list_contents", "rsync_paths"]

logging.getLogger(__name__).addHandler(logging.NullHandler())
