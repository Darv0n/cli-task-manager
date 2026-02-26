"""Tests for the Task model."""

from datetime import date

import pytest
from pydantic import ValidationError

from task_manager.contracts import Priority, Status
from task_manager.models import Task


class TestTaskCreation:
    def test_minimal_task(self):
        task = Task(title="Test task")
        assert task.title == "Test task"
        assert task.status == Status.OPEN
        assert task.priority == Priority.MEDIUM
        assert task.tags == []
        assert task.project is None
        assert task.due_date is None
        assert len(task.id) == 26  # ULID length

    def test_full_task(self):
        task = Task(
            title="Full task",
            description="A task with all fields",
            priority="high",
            tags=["dev", "urgent"],
            project="myproject",
            context="office",
            due_date="2025-12-31",
        )
        assert task.priority == Priority.HIGH
        assert task.tags == ["dev", "urgent"]
        assert task.project == "myproject"
        assert task.due_date == date(2025, 12, 31)

    def test_empty_title_rejected(self):
        with pytest.raises(ValidationError):
            Task(title="")

    def test_title_whitespace_stripped(self):
        task = Task(title="  hello  ")
        assert task.title == "hello"


class TestTagNormalization:
    def test_comma_string_split(self):
        task = Task(title="x", tags="foo, bar, baz")
        assert task.tags == ["foo", "bar", "baz"]

    def test_lowercase_normalization(self):
        task = Task(title="x", tags=["FOO", "Bar"])
        assert task.tags == ["foo", "bar"]

    def test_empty_tags_filtered(self):
        task = Task(title="x", tags="foo,,, bar")
        assert task.tags == ["foo", "bar"]


class TestSigilStripping:
    def test_project_plus_prefix(self):
        task = Task(title="x", project="+myproject")
        assert task.project == "myproject"

    def test_context_at_prefix(self):
        task = Task(title="x", context="@home")
        assert task.context == "home"

    def test_no_prefix_passthrough(self):
        task = Task(title="x", project="myproject")
        assert task.project == "myproject"

    def test_empty_after_strip_becomes_none(self):
        task = Task(title="x", project="+")
        assert task.project is None


class TestSerialization:
    def test_roundtrip(self, sample_task):
        data = sample_task.to_storage()
        restored = Task.from_storage(data)
        assert restored.title == sample_task.title
        assert restored.priority == sample_task.priority
        assert restored.tags == sample_task.tags
        assert restored.due_date == sample_task.due_date

    def test_to_storage_uses_enum_values(self, sample_task):
        data = sample_task.to_storage()
        assert data["status"] == "open"
        assert data["priority"] == "high"

    def test_to_storage_date_as_iso_string(self, sample_task):
        data = sample_task.to_storage()
        assert data["due_date"] == "2025-12-31"
