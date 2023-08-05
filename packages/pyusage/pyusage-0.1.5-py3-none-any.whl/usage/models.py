from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel


class Error(BaseModel):
    """Schema for an error.

    An ``Error`` object corresponds to an error made from a user call.
    The traceback is pruned such that user function calls are omitted.
    Additionally, secrets are also pruned from the traceback message.

    Attributes:
        line: The line on which the error was raised.
        module: The name of the module in which the error was raised.
        traceback: The traceback message of the error.
    """

    traceback: str
    line: int
    module: str
    type: str


class Call(BaseModel):
    """Model for a function call.

    Attributes:
        error: An error, if an error has been raised in this function call.
    """

    error: Optional[Error] = None


class Function(BaseModel):
    """Model for a function.

    Each ``Function`` object corresponds to a method in the developer source code being
    collected by our framework.

    Attributes:
        name: The qualified name of the function.
        labels: A list of labels to categorize the function being tracked.
        calls: A list of calls to this function.
    """

    name: str
    labels: Optional[List[str]] = None
    calls: Optional[List[Call]] = None


class Session(BaseModel):
    """Model for a session.

    A ``Session`` object contains the collected function call history from a
    single program run.

    Attributes:
        uid: A string unique identifier of the user.
        functions: A dictionary of the various tracked functions that were
                   called.
        metadata: A dictionary of global metadata for the session.
    """

    functions: List[Function]
    metadata: Optional[Dict[str, str]] = None
