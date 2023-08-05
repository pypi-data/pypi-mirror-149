import inspect
import os
import pathlib
import sys
import types

import importlib_metadata


def get_package_name(func):
    """Returns the root package name of a function."""
    if isinstance(func, types.BuiltinFunctionType):
        raise ValueError("Can not get package name of built in function.")
    path = inspect.getfile(func)
    if "/" not in path:
        return path[:-3]
    dist = _get_distribution(path)
    if dist:
        return dist.metadata["Name"]
    dirs = path[:-3].split("/")
    module_name = dirs[-1]
    dirs = dirs[:-1]
    cur_path = "/"
    for k, dir_name in enumerate(dirs):
        if dir_name == "site-packages" and k + 1 < len(dirs):
            return dirs[k + 1]
        cur_path = os.path.join(cur_path, dir_name)
        if _contains_init_file(cur_path):
            return dir_name
    version = sys.version_info
    if dirs[-1] in [
        f"python{version.major}",
        f"python{version.major}.{version.minor}",
        f"python{version.major}.{version.minor}.{version.micro}",
    ]:
        raise ValueError("Can not collect standard Python utility")
    return module_name


def _get_distribution(file_name):
    """Get distribution of a file.

    This primarily supports third-party packages installed by PyPA tools. It does not
    support pacakges in the stdlib or packages installed without metadata.
    """
    result = None
    for distribution in importlib_metadata.distributions():
        try:
            relative = pathlib.Path(file_name).relative_to(distribution.locate_file(""))
        except ValueError:
            pass
        else:
            if relative in distribution.files:
                result = distribution
    return result


def _contains_init_file(dir):
    """Checks if a directory contains the __init__.py file."""
    for f in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, f)) and f == "__init__.py":
            return True
    return False
