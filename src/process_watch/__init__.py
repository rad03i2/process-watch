"""Process Watch public API."""

from .core import ProcessInfo, collect_processes, watch_processes

__all__ = ["ProcessInfo", "collect_processes", "watch_processes"]
__version__ = "1.0.0"
