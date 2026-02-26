"""Hook registry — the event bus between core and plugins.

Synchronous, ordered dispatch. Handlers receive a copy of the payload.
Exceptions in handlers are caught and logged — a plugin crash never aborts the user's operation.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from copy import deepcopy

from task_manager.contracts import HookEvent, HookHandler, TaskData


class DefaultHookRegistry:
    def __init__(self) -> None:
        self._handlers: dict[HookEvent, list[HookHandler]] = defaultdict(list)

    def on(self, event: HookEvent, handler: HookHandler) -> None:
        self._handlers[event].append(handler)

    def emit(self, event: HookEvent, payload: TaskData) -> None:
        payload_copy = deepcopy(payload)
        for handler in self._handlers[event]:
            try:
                handler(event, payload_copy)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[task-manager] Plugin hook error on {event!r}: {exc}",
                    file=sys.stderr,
                )
