"""Tests for configuration loading."""

from task_manager.config import Settings


def test_default_settings(monkeypatch, tmp_path):
    """Settings.load() with no config file or env vars should use defaults."""
    monkeypatch.setattr("task_manager.config.CONFIG_FILE", tmp_path / "nonexistent.toml")
    settings = Settings.load()
    assert settings.storage_backend == "json"
    assert settings.default_priority == "medium"
    assert settings.rich_output is True


def test_env_override(monkeypatch, tmp_path):
    monkeypatch.setattr("task_manager.config.CONFIG_FILE", tmp_path / "nonexistent.toml")
    monkeypatch.setenv("TASK_STORAGE_BACKEND", "sqlite")
    settings = Settings.load()
    assert settings.storage_backend == "sqlite"


def test_validate_bad_priority(monkeypatch, tmp_path):
    monkeypatch.setattr("task_manager.config.CONFIG_FILE", tmp_path / "nonexistent.toml")
    monkeypatch.setenv("TASK_DEFAULT_PRIORITY", "extreme")
    settings = Settings.load()
    errors = settings.validate()
    assert len(errors) == 1
    assert "extreme" in errors[0]


def test_validate_good_priority(monkeypatch, tmp_path):
    monkeypatch.setattr("task_manager.config.CONFIG_FILE", tmp_path / "nonexistent.toml")
    settings = Settings.load()
    errors = settings.validate()
    assert errors == []
