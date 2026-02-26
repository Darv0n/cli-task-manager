"""Task filtering predicates — shared between storage backends."""

from __future__ import annotations

from typing import Any


def apply_filters(
    tasks: list[dict[str, Any]],
    *,
    status: list[str] | None = None,
    priority: list[str] | None = None,
    tags: list[str] | None = None,
    project: str | None = None,
    context: str | None = None,
) -> list[dict[str, Any]]:
    """Filter a list of task dicts by the given criteria. All filters are AND-combined."""
    result = tasks

    if status:
        status_set = set(status)
        result = [t for t in result if t.get("status") in status_set]

    if priority:
        priority_set = set(priority)
        result = [t for t in result if t.get("priority") in priority_set]

    if tags:
        tag_set = set(tags)
        result = [t for t in result if tag_set.issubset(set(t.get("tags", [])))]

    if project is not None:
        result = [t for t in result if t.get("project") == project]

    if context is not None:
        result = [t for t in result if t.get("context") == context]

    return result
