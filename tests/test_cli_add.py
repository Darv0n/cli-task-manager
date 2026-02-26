"""Tests for the add CLI command."""

from typer.testing import CliRunner

from task_manager.cli.app import app
from task_manager.storage.json_backend import JsonBackend

runner = CliRunner()


def test_add_basic(tmp_path):
    result = runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "add", "Test task"])
    assert result.exit_code == 0
    assert "Created" in result.output
    assert "Test task" in result.output


def test_add_with_options(tmp_path):
    result = runner.invoke(
        app,
        [
            "--data-dir",
            str(tmp_path),
            "--no-plugins",
            "add",
            "Full task",
            "--priority",
            "high",
            "--tags",
            "dev,urgent",
            "--project",
            "myproject",
            "--due",
            "2025-12-31",
        ],
    )
    assert result.exit_code == 0
    assert "Created" in result.output

    # Verify the task was actually stored
    backend = JsonBackend(data_dir=tmp_path)
    tasks = backend.list()
    assert len(tasks) == 1
    assert tasks[0]["priority"] == "high"
    assert tasks[0]["tags"] == ["dev", "urgent"]
