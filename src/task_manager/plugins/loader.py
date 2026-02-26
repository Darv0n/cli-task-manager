"""Plugin loader: directory scan + importlib.

Convention:
  - Each .py file in plugins_dir is a potential plugin module.
  - Must have a top-level `plugin` variable implementing the Plugin protocol.
  - The loader calls plugin.register(hooks) for each loaded plugin.
  - Bad plugins log to stderr and are skipped.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from task_manager.contracts import Plugin
from task_manager.plugins.hooks import DefaultHookRegistry


def load_plugins(
    plugins_dir: Path,
    hooks: DefaultHookRegistry,
    *,
    silent: bool = False,
) -> list[str]:
    """Load all plugins from plugins_dir. Returns list of loaded plugin names."""
    loaded: list[str] = []

    if not plugins_dir.exists():
        return loaded

    for plugin_file in sorted(plugins_dir.glob("*.py")):
        module_name = f"task_manager_plugin_{plugin_file.stem}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, plugin_file)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not create module spec for {plugin_file}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            plugin = getattr(module, "plugin", None)
            if plugin is None:
                raise ImportError("Module has no top-level 'plugin' variable")
            if not isinstance(plugin, Plugin):
                raise ImportError(
                    "'plugin' variable does not implement Plugin protocol "
                    "(missing: name, version, or register)"
                )

            plugin.register(hooks)
            loaded.append(plugin.name)

        except Exception as exc:  # noqa: BLE001
            if not silent:
                print(
                    f"[task-manager] Plugin load failed [{plugin_file}]: {exc}",
                    file=sys.stderr,
                )

    return loaded
