from pathlib import Path
from ._vendor.single_source import get_version

root_package_name = __name__.split(".")[0]
# This is actually somewhat unreliable.
#
# The logic implemented here is:
# 1) search for pyproject.toml at Path(__file__).parent.parent.
# 2) if found, use the version in the toml file. Otherwise, use importlib_metadata to find the installed Terality version.
#
# However, sometimes a stray pyproject.toml may be present at Path(__file__).parent.parent that's completely unrelated to Terality.
# For instance, installing `https://github.com/JBKahn/flake8-print` puts the pyproject.toml of this project in the site-packages root, and `get_version` picks up this pyproject.toml instead of relying on importlib_metadata.
#
# We don't wait to add a TOML parser as a dependency, nor have complex logic here, so
# for now we'll just ignore the issue.
__version__ = get_version(root_package_name, Path(__file__).parent.parent)
