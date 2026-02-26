"""SQLite storage backend.

Schema: tasks table with columns matching Task model fields.
Tags stored as JSON text column (sqlite has no array type).
Thread safety: each call opens a new connection with WAL mode.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from task_manager.errors import StorageUnavailable, TaskNotFound

from . import register_backend

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id          TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'open',
    priority    TEXT NOT NULL DEFAULT 'medium',
    tags        TEXT NOT NULL DEFAULT '[]',
    project     TEXT,
    context     TEXT,
    due_date    TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project);
"""


class SqliteBackend:
    name: str = "sqlite"

    def __init__(self, *, data_dir: Path) -> None:
        self._db_path = Path(data_dir) / "tasks.db"
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(str(self._db_path))
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            return conn
        except sqlite3.Error as exc:
            raise StorageUnavailable(f"Cannot open SQLite DB: {exc}") from exc

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        d = dict(row)
        d["tags"] = json.loads(d["tags"])
        return d

    def _dict_to_params(self, data: dict[str, Any]) -> dict[str, Any]:
        return {**data, "tags": json.dumps(data.get("tags", []))}

    def get(self, task_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return self._row_to_dict(row) if row else None

    def list(
        self,
        *,
        status: list[str] | None = None,
        priority: list[str] | None = None,
        tags: list[str] | None = None,
        project: str | None = None,
        context: str | None = None,
    ) -> list[dict[str, Any]]:
        where_clauses: list[str] = []
        params: list[str] = []

        if status:
            placeholders = ",".join("?" * len(status))
            where_clauses.append(f"status IN ({placeholders})")
            params.extend(status)

        if priority:
            placeholders = ",".join("?" * len(priority))
            where_clauses.append(f"priority IN ({placeholders})")
            params.extend(priority)

        if project is not None:
            where_clauses.append("project = ?")
            params.append(project)

        if context is not None:
            where_clauses.append("context = ?")
            params.append(context)

        sql = "SELECT * FROM tasks"
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY created_at ASC"

        with self._connect() as conn:
            rows = conn.execute(sql, params).fetchall()
            results = [self._row_to_dict(r) for r in rows]

        # Tags filter in Python — SQLite JSON1 extension not guaranteed
        if tags:
            tag_set = set(tags)
            results = [r for r in results if tag_set.issubset(set(r["tags"]))]

        return results

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        params = self._dict_to_params(data)
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO tasks
                   (id, title, description, status, priority, tags,
                    project, context, due_date, created_at, updated_at)
                   VALUES
                   (:id, :title, :description, :status, :priority, :tags,
                    :project, :context, :due_date, :created_at, :updated_at)""",
                params,
            )
        return data

    def update(self, task_id: str, patch: dict[str, Any]) -> dict[str, Any]:
        existing = self.get(task_id)
        if existing is None:
            raise TaskNotFound(task_id)
        merged = {**existing, **patch}
        params = self._dict_to_params(merged)
        params["id"] = task_id
        with self._connect() as conn:
            conn.execute(
                """UPDATE tasks SET
                   title=:title, description=:description, status=:status,
                   priority=:priority, tags=:tags, project=:project,
                   context=:context, due_date=:due_date, updated_at=:updated_at
                   WHERE id=:id""",
                params,
            )
        return merged

    def delete(self, task_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0

    def search(self, query: str) -> list[dict[str, Any]]:
        q = f"%{query}%"
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?",
                (q, q),
            ).fetchall()
        return [self._row_to_dict(r) for r in rows]


register_backend("sqlite", SqliteBackend)
