import platform
from typing import Dict

from .decorators import collect, metadata

__version__ = "0.1.5"
__author__ = "The PyUsage Team"
__copyright__ = f"Copyright 2022 {__author__}"


collect = collect(collect)
metadata = collect(metadata)


@metadata
def _get_metadata() -> Dict[str, str]:
    return {
        "python": platform.python_version(),
        "os": platform.system(),
        "version": __version__,
    }
