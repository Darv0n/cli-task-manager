"""Tests for JSON storage backend."""

import pytest

from task_manager.errors import TaskNotFound


class TestJsonBackendCrud:
    def test_create_and_get(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        result = json_backend.get(sample_task_data["id"])
        assert result is not None
        assert result["title"] == sample_task_data["title"]

    def test_get_nonexistent(self, json_backend):
        assert json_backend.get("nonexistent") is None

    def test_list_empty(self, json_backend):
        assert json_backend.list() == []

    def test_list_all(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        results = json_backend.list()
        assert len(results) == 1

    def test_update(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        updated = json_backend.update(sample_task_data["id"], {"title": "Updated"})
        assert updated["title"] == "Updated"

    def test_update_nonexistent_raises(self, json_backend):
        with pytest.raises(TaskNotFound):
            json_backend.update("nonexistent", {"title": "x"})

    def test_delete(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        assert json_backend.delete(sample_task_data["id"]) is True
        assert json_backend.get(sample_task_data["id"]) is None

    def test_delete_nonexistent(self, json_backend):
        assert json_backend.delete("nonexistent") is False

    def test_search(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        results = json_backend.search("groceries")
        assert len(results) == 1

    def test_search_no_match(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        results = json_backend.search("zzzzz")
        assert len(results) == 0


class TestJsonBackendFilters:
    def test_filter_by_status(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        results = json_backend.list(status=["open"])
        assert len(results) == 1
        results = json_backend.list(status=["done"])
        assert len(results) == 0

    def test_filter_by_tags(self, json_backend, sample_task_data):
        json_backend.create(sample_task_data)
        results = json_backend.list(tags=["shopping"])
        assert len(results) == 1
        results = json_backend.list(tags=["nonexistent"])
        assert len(results) == 0
