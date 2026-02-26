"""Tests for task filtering predicates."""

from task_manager.utils.filters import apply_filters

TASKS = [
    {"id": "1", "status": "open", "priority": "high", "tags": ["dev", "urgent"], "project": "a"},
    {"id": "2", "status": "done", "priority": "low", "tags": ["docs"], "project": "a"},
    {"id": "3", "status": "open", "priority": "medium", "tags": ["dev"], "project": "b"},
    {"id": "4", "status": "cancelled", "priority": "high", "tags": [], "project": None},
]


def test_no_filters_returns_all():
    assert len(apply_filters(TASKS)) == 4


def test_filter_by_status():
    result = apply_filters(TASKS, status=["open"])
    assert len(result) == 2


def test_filter_by_multiple_status():
    result = apply_filters(TASKS, status=["open", "done"])
    assert len(result) == 3


def test_filter_by_priority():
    result = apply_filters(TASKS, priority=["high"])
    assert len(result) == 2


def test_filter_by_tags_subset():
    result = apply_filters(TASKS, tags=["dev"])
    assert len(result) == 2


def test_filter_by_tags_exact():
    result = apply_filters(TASKS, tags=["dev", "urgent"])
    assert len(result) == 1


def test_filter_by_project():
    result = apply_filters(TASKS, project="a")
    assert len(result) == 2


def test_combined_filters():
    result = apply_filters(TASKS, status=["open"], priority=["high"])
    assert len(result) == 1
    assert result[0]["id"] == "1"
