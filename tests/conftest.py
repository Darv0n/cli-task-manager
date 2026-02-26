"""Shared fixtures for task manager tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from task_manager.models import Task
from task_manager.storage.json_backend import JsonBackend
from task_manager.storage.sqlite_backend import SqliteBackend


@pytest.fixture()
def tmp_data_dir(tmp_path: Path) -> Path:
    """Provide a temporary data directory for storage tests."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture()
def json_backend(tmp_data_dir: Path) -> JsonBackend:
    return JsonBackend(data_dir=tmp_data_dir)


@pytest.fixture()
def sqlite_backend(tmp_data_dir: Path) -> SqliteBackend:
    return SqliteBackend(data_dir=tmp_data_dir)


@pytest.fixture()
def sample_task() -> Task:
    return Task(
        title="Buy groceries",
        description="Milk, eggs, bread",
        priority="high",
        tags=["shopping", "errands"],
        project="home",
        context="store",
        due_date="2025-12-31",
    )


@pytest.fixture()
def sample_task_data(sample_task: Task) -> dict:
    return sample_task.to_storage()
