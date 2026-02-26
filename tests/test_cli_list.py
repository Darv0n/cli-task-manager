"""Tests for the list CLI command."""

from typer.testing import CliRunner

from task_manager.cli.app import app

# Rich uses COLUMNS to determine terminal width; set wide enough for table rendering
runner = CliRunner(env={"COLUMNS": "200"})


def test_list_empty(tmp_path):
    result = runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "list"])
    assert result.exit_code == 0
    assert "No tasks found" in result.output


def test_list_after_add(tmp_path):
    runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "add", "Task 1"])
    runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "add", "Task 2"])
    result = runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "list"])
    assert result.exit_code == 0
    assert "Task 1" in result.output
    assert "Task 2" in result.output


def test_list_filter_status(tmp_path):
    runner.invoke(app, ["--data-dir", str(tmp_path), "--no-plugins", "add", "Open task"])
    result = runner.invoke(
        app, ["--data-dir", str(tmp_path), "--no-plugins", "list", "--status", "done"]
    )
    assert result.exit_code == 0
    assert "No tasks found" in result.output
