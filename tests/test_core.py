from types import SimpleNamespace

import pytest

from process_watch.core import collect_processes, watch_processes


class FakeProcess:
    def __init__(self, **info):
        self.info = info


def fake_iter(*, attrs):
    assert "cpu_percent" in attrs
    return [
        FakeProcess(pid=10, name="python", username="alice", status="running", cpu_percent=12.5,
                    memory_percent=2.5, memory_info=SimpleNamespace(rss=2048), create_time=1_700_000_000),
        FakeProcess(pid=20, name="Browser", username="bob", status="sleeping", cpu_percent=1.0,
                    memory_percent=8.0, memory_info=SimpleNamespace(rss=4096), create_time=1_700_000_100),
        FakeProcess(pid=30, name="python-worker", username="alice", status="running", cpu_percent=50.0,
                    memory_percent=4.0, memory_info=SimpleNamespace(rss=8192), create_time=1_700_000_200),
    ]


def test_collect_filters_and_sorts():
    rows = collect_processes(name="PYTHON", user="ALI", sort_by="cpu", limit=10, process_iter=fake_iter)
    assert [p.pid for p in rows] == [30, 10]
    assert rows[0].memory_rss == 8192
    assert rows[0].created_at.endswith("+00:00")


def test_memory_threshold_and_sort():
    rows = collect_processes(min_memory=3, sort_by="memory", limit=10, process_iter=fake_iter)
    assert [p.pid for p in rows] == [20, 30]


@pytest.mark.parametrize("kwargs", [
    {"limit": 0}, {"limit": 1001}, {"min_cpu": -1}, {"min_memory": -1}, {"sort_by": "bad"}
])
def test_invalid_snapshot_options(kwargs):
    with pytest.raises(ValueError):
        collect_processes(process_iter=fake_iter, **kwargs)


def test_watch_validation():
    with pytest.raises(ValueError):
        next(watch_processes(interval=0.1, count=1))
    with pytest.raises(ValueError):
        next(watch_processes(interval=1, count=0))
