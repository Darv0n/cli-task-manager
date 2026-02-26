"""Storage backend registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from task_manager.contracts import StorageBackend

_REGISTRY: dict[str, type] = {}


def register_backend(name: str, cls: type) -> None:
    _REGISTRY[name] = cls


def get_backend(name: str, **kwargs: object) -> "StorageBackend":
    if name not in _REGISTRY:
        from task_manager.errors import BackendNotFound

        available = ", ".join(_REGISTRY) or "(none)"
        raise BackendNotFound(f"Unknown storage backend {name!r}. Available: {available}")
    return _REGISTRY[name](**kwargs)


def available_backends() -> list[str]:
    return list(_REGISTRY)
