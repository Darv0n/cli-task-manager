"""Settings: TOML file + env var overlay.

Resolution order (highest to lowest priority):
  1. Environment variables (TASK_STORAGE_BACKEND, TASK_DATA_DIR, etc.)
  2. ~/.task-manager/config.toml
  3. Built-in defaults
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".task-manager"
CONFIG_FILE = CONFIG_DIR / "config.toml"
PLUGINS_DIR = CONFIG_DIR / "plugins"


def _load_toml() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)
    return {}


@dataclass(frozen=True)
class Settings:
    storage_backend: str
    data_dir: Path
    plugins_dir: Path
    default_priority: str
    date_format: str
    rich_output: bool

    @classmethod
    def load(cls) -> Settings:
        toml = _load_toml()
        storage = toml.get("storage", {})
        display = toml.get("display", {})
        return cls(
            storage_backend=os.environ.get(
                "TASK_STORAGE_BACKEND",
                storage.get("backend", "json"),
            ),
            data_dir=Path(
                os.environ.get(
                    "TASK_DATA_DIR",
                    storage.get("data_dir", str(CONFIG_DIR / "data")),
                )
            ),
            plugins_dir=Path(
                os.environ.get(
                    "TASK_PLUGINS_DIR",
                    str(toml.get("plugins_dir", str(PLUGINS_DIR))),
                )
            ),
            default_priority=os.environ.get(
                "TASK_DEFAULT_PRIORITY",
                toml.get("default_priority", "medium"),
            ),
            date_format=os.environ.get(
                "TASK_DATE_FORMAT",
                display.get("date_format", "%Y-%m-%d"),
            ),
            rich_output=os.environ.get(
                "TASK_RICH_OUTPUT",
                str(display.get("rich_output", "true")),
            ).lower()
            == "true",
        )

    def validate(self) -> list[str]:
        errors = []
        from task_manager.contracts import Priority

        valid_priorities = {p.value for p in Priority}
        if self.default_priority not in valid_priorities:
            errors.append(
                f"default_priority must be one of {valid_priorities}, got '{self.default_priority}'"
            )
        return errors
