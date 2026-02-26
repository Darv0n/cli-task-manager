"""JSON file storage backend.

Data layout: single file, tasks stored as a dict keyed by ID.
  { "tasks": { "<id>": { ...task fields... }, ... } }

Write strategy: write to .tmp, then replace. Atomic on POSIX, safe on Windows.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from task_manager.errors import StorageCorrupt, StorageUnavailable, TaskNotFound
from task_manager.utils.filters import apply_filters

from . import register_backend


class JsonBackend:
    name: str = "json"

    def __init__(self, *, data_dir: Path) -> None:
        self._path = Path(data_dir) / "tasks.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict[str, Any]:
        if not self._path.exists():
            return {"tasks": {}}
        try:
            text = self._path.read_text(encoding="utf-8")
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise StorageCorrupt(f"tasks.json is not valid JSON: {exc}") from exc
        except OSError as exc:
            raise StorageUnavailable(f"Cannot read tasks.json: {exc}") from exc

    def _save(self, data: dict[str, Any]) -> None:
        tmp = self._path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
            tmp.replace(self._path)
        except OSError as exc:
            raise StorageUnavailable(f"Cannot write tasks.json: {exc}") from exc

    def get(self, task_id: str) -> dict[str, Any] | None:
        data = self._load()
        return data["tasks"].get(task_id)

    def list(
        self,
        *,
        status: list[str] | None = None,
        priority: list[str] | None = None,
        tags: list[str] | None = None,
        project: str | None = None,
        context: str | None = None,
    ) -> list[dict[str, Any]]:
        data = self._load()
        tasks = list(data["tasks"].values())
        return apply_filters(
            tasks,
            status=status,
            priority=priority,
            tags=tags,
            project=project,
            context=context,
        )

    def create(self, task_data: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        task_id = task_data["id"]
        data["tasks"][task_id] = task_data
        self._save(data)
        return task_data

    def update(self, task_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        if task_id not in data["tasks"]:
            raise TaskNotFound(task_id)
        data["tasks"][task_id].update(patch)
        self._save(data)
        return data["tasks"][task_id]

    def delete(self, task_id: str) -> bool:
        data = self._load()
        if task_id not in data["tasks"]:
            return False
        del data["tasks"][task_id]
        self._save(data)
        return True

    def search(self, query: str) -> list[dict[str, Any]]:
        data = self._load()
        q = query.lower()
        return [
            t
            for t in data["tasks"].values()
            if q in t.get("title", "").lower()
            or q in t.get("description", "").lower()
            or any(q in tag for tag in t.get("tags", []))
        ]


register_backend("json", JsonBackend)
