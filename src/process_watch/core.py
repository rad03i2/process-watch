"""Core process inspection and monitoring logic."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import time
from typing import Callable, Iterator, Sequence

import psutil


@dataclass(frozen=True, slots=True)
class ProcessInfo:
    pid: int
    name: str
    username: str | None
    status: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    created_at: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _iso_timestamp(value: float | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    except (OSError, OverflowError, ValueError):
        return None


def collect_processes(
    *,
    name: str | None = None,
    user: str | None = None,
    min_cpu: float = 0.0,
    min_memory: float = 0.0,
    sort_by: str = "cpu",
    limit: int = 20,
    process_iter: Callable[..., Sequence[object]] | None = None,
) -> list[ProcessInfo]:
    """Return a filtered, sorted snapshot of visible local processes.

    Processes that disappear or become inaccessible during collection are skipped.
    """
    if min_cpu < 0 or min_memory < 0:
        raise ValueError("minimum CPU and memory values must be non-negative")
    if limit < 1 or limit > 1000:
        raise ValueError("limit must be between 1 and 1000")
    if sort_by not in {"cpu", "memory", "pid", "name"}:
        raise ValueError("sort_by must be one of: cpu, memory, pid, name")

    iterator = process_iter or psutil.process_iter
    attrs = ["pid", "name", "username", "status", "cpu_percent", "memory_percent", "memory_info", "create_time"]
    rows: list[ProcessInfo] = []
    needle = name.casefold() if name else None
    user_needle = user.casefold() if user else None

    for proc in iterator(attrs=attrs):
        try:
            info = proc.info  # type: ignore[attr-defined]
            proc_name = str(info.get("name") or "<unknown>")
            username = info.get("username")
            username = str(username) if username else None
            if needle and needle not in proc_name.casefold():
                continue
            if user_needle and (username is None or user_needle not in username.casefold()):
                continue
            cpu = float(info.get("cpu_percent") or 0.0)
            memory = float(info.get("memory_percent") or 0.0)
            if cpu < min_cpu or memory < min_memory:
                continue
            mem_info = info.get("memory_info")
            rss = int(getattr(mem_info, "rss", 0) or 0)
            rows.append(ProcessInfo(
                pid=int(info["pid"]),
                name=proc_name,
                username=username,
                status=str(info.get("status") or "unknown"),
                cpu_percent=round(cpu, 2),
                memory_percent=round(memory, 2),
                memory_rss=rss,
                created_at=_iso_timestamp(info.get("create_time")),
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, KeyError, TypeError, ValueError):
            continue

    key = {
        "cpu": lambda p: (-p.cpu_percent, p.pid),
        "memory": lambda p: (-p.memory_percent, p.pid),
        "pid": lambda p: (p.pid,),
        "name": lambda p: (p.name.casefold(), p.pid),
    }[sort_by]
    rows.sort(key=key)
    return rows[:limit]


def watch_processes(*, interval: float = 2.0, count: int | None = None, **filters: object) -> Iterator[list[ProcessInfo]]:
    """Yield process snapshots at a controlled interval."""
    if interval < 0.2 or interval > 3600:
        raise ValueError("interval must be between 0.2 and 3600 seconds")
    if count is not None and (count < 1 or count > 100000):
        raise ValueError("count must be between 1 and 100000")
    iteration = 0
    while count is None or iteration < count:
        yield collect_processes(**filters)
        iteration += 1
        if count is None or iteration < count:
            time.sleep(interval)
