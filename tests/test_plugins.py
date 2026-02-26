"""Tests for the plugin system."""

from task_manager.contracts import HookEvent
from task_manager.plugins.hooks import DefaultHookRegistry
from task_manager.plugins.loader import load_plugins


def test_hook_registry_emit():
    registry = DefaultHookRegistry()
    received = []

    def handler(event, payload):
        received.append((event, payload))

    registry.on(HookEvent.TASK_CREATED, handler)
    registry.emit(HookEvent.TASK_CREATED, {"id": "test"})

    assert len(received) == 1
    assert received[0][0] == HookEvent.TASK_CREATED


def test_hook_handler_exception_isolated():
    """A bad handler should not crash the registry."""
    registry = DefaultHookRegistry()
    received = []

    def bad_handler(event, payload):
        raise RuntimeError("boom")

    def good_handler(event, payload):
        received.append(payload)

    registry.on(HookEvent.TASK_CREATED, bad_handler)
    registry.on(HookEvent.TASK_CREATED, good_handler)
    registry.emit(HookEvent.TASK_CREATED, {"id": "test"})

    assert len(received) == 1  # good_handler still ran


def test_hook_payload_is_copy():
    """Handlers receive a copy — mutations don't affect caller."""
    registry = DefaultHookRegistry()

    def mutating_handler(event, payload):
        payload["id"] = "mutated"

    registry.on(HookEvent.TASK_CREATED, mutating_handler)

    original = {"id": "original"}
    registry.emit(HookEvent.TASK_CREATED, original)
    assert original["id"] == "original"


def test_load_plugins_empty_dir(tmp_path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    hooks = DefaultHookRegistry()
    loaded = load_plugins(plugins_dir, hooks, silent=True)
    assert loaded == []


def test_load_plugins_nonexistent_dir(tmp_path):
    hooks = DefaultHookRegistry()
    loaded = load_plugins(tmp_path / "nonexistent", hooks, silent=True)
    assert loaded == []


def test_load_valid_plugin(tmp_path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    plugin_code = """
class MyPlugin:
    name = "test-plugin"
    version = "0.1.0"

    def register(self, hooks):
        pass

plugin = MyPlugin()
"""
    (plugins_dir / "test_plugin.py").write_text(plugin_code)

    hooks = DefaultHookRegistry()
    loaded = load_plugins(plugins_dir, hooks, silent=True)
    assert loaded == ["test-plugin"]


def test_load_bad_plugin_skipped(tmp_path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()

    (plugins_dir / "bad_plugin.py").write_text("raise RuntimeError('broken')")

    hooks = DefaultHookRegistry()
    loaded = load_plugins(plugins_dir, hooks, silent=True)
    assert loaded == []
