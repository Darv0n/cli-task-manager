"""Protocol compliance tests — both backends must pass identical suite."""

import pytest

from task_manager.models import Task
from task_manager.storage.json_backend import JsonBackend
from task_manager.storage.sqlite_backend import SqliteBackend


@pytest.fixture(params=["json", "sqlite"])
def backend(request, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    if request.param == "json":
        return JsonBackend(data_dir=data_dir)
    return SqliteBackend(data_dir=data_dir)


def _make_task(**kwargs) -> dict:
    return Task(title="Test task", **kwargs).to_storage()


class TestProtocolCompliance:
    def test_create_and_retrieve(self, backend):
        data = _make_task()
        backend.create(data)
        result = backend.get(data["id"])
        assert result["title"] == "Test task"

    def test_list_returns_list(self, backend):
        assert isinstance(backend.list(), list)

    def test_update_returns_merged(self, backend):
        data = _make_task()
        backend.create(data)
        updated = backend.update(data["id"], {"title": "Changed"})
        assert updated["title"] == "Changed"

    def test_delete_returns_bool(self, backend):
        data = _make_task()
        backend.create(data)
        assert backend.delete(data["id"]) is True
        assert backend.delete(data["id"]) is False

    def test_search_returns_list(self, backend):
        assert isinstance(backend.search("anything"), list)

    def test_roundtrip_preserves_tags(self, backend):
        data = _make_task(tags=["a", "b", "c"])
        backend.create(data)
        result = backend.get(data["id"])
        assert result["tags"] == ["a", "b", "c"]

    def test_filter_by_status(self, backend):
        data = _make_task()
        backend.create(data)
        assert len(backend.list(status=["open"])) == 1
        assert len(backend.list(status=["done"])) == 0

    def test_filter_by_project(self, backend):
        data = _make_task(project="myproject")
        backend.create(data)
        assert len(backend.list(project="myproject")) == 1
        assert len(backend.list(project="other")) == 0
