"""Error hierarchy for task-manager.

Naming convention: structural cause, not symptom.
  TaskNotFound not TaskLookupError
  StorageCorrupt not DataError
  ValidationRejected not BadInputError
"""


class TaskManagerError(Exception):
    """Root. Every error in this system derives from this."""

    exit_code: int = 1


# --- Storage layer ---


class StorageError(TaskManagerError):
    """Base for all storage-layer failures."""


class StorageCorrupt(StorageError):
    """Storage data is present but cannot be parsed."""

    exit_code = 2


class StorageUnavailable(StorageError):
    """Storage backend cannot be reached (file locked, DB down, etc.)."""

    exit_code = 3


class BackendNotFound(StorageError):
    """Requested storage backend name is not registered."""

    exit_code = 4


# --- Domain layer ---


class TaskNotFound(TaskManagerError):
    """No task exists with the given ID (or ID prefix)."""

    exit_code = 10

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task not found: {task_id!r}")


class AmbiguousTaskId(TaskManagerError):
    """ID prefix matches more than one task."""

    exit_code = 11

    def __init__(self, prefix: str, matches: list[str]) -> None:
        self.prefix = prefix
        self.matches = matches
        super().__init__(f"Prefix {prefix!r} is ambiguous — matches: {', '.join(matches)}")


class ValidationRejected(TaskManagerError):
    """Input failed domain validation before reaching storage."""

    exit_code = 20


# --- Config layer ---


class ConfigError(TaskManagerError):
    """Base for configuration failures."""

    exit_code = 30


class ConfigInvalid(ConfigError):
    """Config file exists but contains invalid values."""

    exit_code = 31


# --- Plugin layer ---


class PluginError(TaskManagerError):
    """Base for plugin loading/execution failures."""

    exit_code = 40


class PluginLoadFailed(PluginError):
    """A plugin file could not be imported or did not implement Plugin protocol."""

    exit_code = 41

    def __init__(self, plugin_path: str, reason: str) -> None:
        self.plugin_path = plugin_path
        super().__init__(f"Plugin load failed [{plugin_path}]: {reason}")
