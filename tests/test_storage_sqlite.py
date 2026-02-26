"""Tests for SQLite storage backend."""

import pytest

from task_manager.errors import TaskNotFound


class TestSqliteBackendCrud:
    def test_create_and_get(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        result = sqlite_backend.get(sample_task_data["id"])
        assert result is not None
        assert result["title"] == sample_task_data["title"]

    def test_get_nonexistent(self, sqlite_backend):
        assert sqlite_backend.get("nonexistent") is None

    def test_list_empty(self, sqlite_backend):
        assert sqlite_backend.list() == []

    def test_list_all(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        results = sqlite_backend.list()
        assert len(results) == 1

    def test_update(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        updated = sqlite_backend.update(sample_task_data["id"], {"title": "Updated"})
        assert updated["title"] == "Updated"

    def test_update_nonexistent_raises(self, sqlite_backend):
        with pytest.raises(TaskNotFound):
            sqlite_backend.update("nonexistent", {"title": "x"})

    def test_delete(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        assert sqlite_backend.delete(sample_task_data["id"]) is True
        assert sqlite_backend.get(sample_task_data["id"]) is None

    def test_delete_nonexistent(self, sqlite_backend):
        assert sqlite_backend.delete("nonexistent") is False

    def test_search(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        results = sqlite_backend.search("groceries")
        assert len(results) == 1

    def test_search_no_match(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        results = sqlite_backend.search("zzzzz")
        assert len(results) == 0


class TestSqliteBackendFilters:
    def test_filter_by_status(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        results = sqlite_backend.list(status=["open"])
        assert len(results) == 1
        results = sqlite_backend.list(status=["done"])
        assert len(results) == 0

    def test_filter_by_tags(self, sqlite_backend, sample_task_data):
        sqlite_backend.create(sample_task_data)
        results = sqlite_backend.list(tags=["shopping"])
        assert len(results) == 1
        results = sqlite_backend.list(tags=["nonexistent"])
        assert len(results) == 0
