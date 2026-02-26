"""Single source of truth for all types, enums, and protocols."""

from __future__ import annotations

from collections.abc import Callable
from enum import Enum
from typing import Any, Protocol, TypeAlias, runtime_checkable


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class HookEvent(str, Enum):
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_DELETED = "task.deleted"
    TASK_COMPLETED = "task.completed"
    BEFORE_LIST = "before.list"


TaskData: TypeAlias = dict[str, Any]
HookHandler: TypeAlias = Callable[[HookEvent, TaskData], None]


@runtime_checkable
class StorageBackend(Protocol):
    """Protocol for pluggable storage implementations.

    All methods are synchronous. The CLI is synchronous and adding async
    here would infect the entire call stack without benefit.
    """

    @property
    def name(self) -> str: ...

    def get(self, task_id: str) -> TaskData | None: ...

    def list(
        self,
        *,
        status: list[str] | None = None,
        priority: list[str] | None = None,
        tags: list[str] | None = None,
        project: str | None = None,
        context: str | None = None,
    ) -> list[TaskData]: ...

    def create(self, data: TaskData) -> TaskData: ...

    def update(self, task_id: str, patch: TaskData) -> TaskData: ...

    def delete(self, task_id: str) -> bool: ...

    def search(self, query: str) -> list[TaskData]: ...


@runtime_checkable
class Plugin(Protocol):
    """Protocol for task manager plugins."""

    name: str
    version: str

    def register(self, hooks: HookRegistry) -> None: ...


@runtime_checkable
class HookRegistry(Protocol):
    def on(self, event: HookEvent, handler: HookHandler) -> None: ...

    def emit(self, event: HookEvent, payload: TaskData) -> None: ...
