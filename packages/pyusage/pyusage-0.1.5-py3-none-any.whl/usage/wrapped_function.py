import sys
import traceback
from typing import Callable, List, Optional

from .models import Call, Error, Function


class WrappedFunction:
    """A something."""

    def __init__(
        self,
        function: Callable,
        labels: Optional[List[str]] = None,
    ):
        """Do something."""
        self._labels = labels if labels is not None else []
        self._name = _get_qualified_name(function)
        self._calls: List[Call] = []

        self._function = function

    def __call__(self, *args, **kwargs):
        """Do something."""
        error = None
        try:
            output = self._function(*args, **kwargs)
            self.calls.append(Call())
            return output
        except Exception as exception:
            error_type, _, error_tb = sys.exc_info()
            filename = error_tb.tb_frame.f_code.co_filename
            line_number = error_tb.tb_lineno
            traceback_msg = traceback.format_exc()
            error = Error(
                traceback=traceback_msg,
                line=line_number,
                module=filename,
                type=error_type.__name__,
            )
            self.calls.append(Call(error=error))
            raise exception

    @property
    def labels(self) -> List[str]:
        """Do something."""
        return self._labels

    @property
    def name(self) -> str:
        """Do something."""
        return self._name

    @property
    def calls(self) -> List[Call]:
        """Do something."""
        return self._calls


def _get_qualified_name(func):
    """Returns the fully qualified name of a function."""
    return f"{func.__module__}.{func.__name__}"
