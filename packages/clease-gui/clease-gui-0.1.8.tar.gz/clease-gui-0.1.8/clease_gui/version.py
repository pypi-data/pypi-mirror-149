# pylint: disable=invalid-name
from pathlib import Path
from packaging.version import parse

__all__ = ("__version__", "version_info")

with Path(__file__).with_name("_version.txt").open("r") as f:
    # A class of type Version
    version_info = parse(f.readline().strip())

__version__ = str(version_info)
