from __future__ import annotations

import atexit
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, Optional, Set

from usage.clients import Client, ProductionClient

from .clients import Client, ProductionClient
from .models import Function
from .models import Session as SessionModel
from .wrapped_function import WrappedFunction

_session = None  # pylint: disable=invalid-name


def is_initialized() -> bool:
    return _session is not None


def init(session: Optional[Session] = None) -> None:
    global _session  # pylint: disable=invalid-name, global-statement
    _session = Session() if session is None else session


def shutdown() -> None:
    if not is_initialized():
        return

    _upload_packages()

    global _session
    assert _session is not None
    _session = None


atexit.register(shutdown)


def get_or_create_session() -> Session:
    if not is_initialized():
        init()

    return _session


@dataclass(frozen=True)
class Session:

    metadata: Dict[str, Optional[Dict[str, str]]] = field(
        default_factory=lambda: defaultdict(lambda: None)
    )
    functions: Dict[str, Set[WrappedFunction]] = field(
        default_factory=lambda: defaultdict(set)
    )
    client: Client = field(default_factory=ProductionClient)


def _upload_packages():
    packages = set(_session.metadata) | set(_session.functions)
    for package in packages:
        session = _get_session_model(package)
        _session.client.upload_session(session, package)


def _get_session_model(package: str) -> SessionModel:
    functions = []
    for wrapped_function in _session.functions[package]:
        function = Function(
            name=wrapped_function.name,
            labels=wrapped_function.labels,
            calls=wrapped_function.calls,
        )
        functions.append(function)

    metadata = _session.metadata[package]

    return SessionModel(functions=functions, metadata=metadata)
