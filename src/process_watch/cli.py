"""Command-line interface for Process Watch."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from . import __version__
from .core import ProcessInfo, collect_processes, watch_processes


def _bytes(value: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{amount:.1f} TiB"


def _print_table(rows: list[ProcessInfo]) -> None:
    if not rows:
        print("No matching processes.")
        return
    print(f"{'PID':>7}  {'CPU%':>7}  {'MEM%':>7}  {'RSS':>10}  {'STATUS':<12}  NAME")
    print("-" * 78)
    for row in rows:
        name = row.name if len(row.name) <= 28 else row.name[:25] + "..."
        print(f"{row.pid:>7}  {row.cpu_percent:>7.2f}  {row.memory_percent:>7.2f}  {_bytes(row.memory_rss):>10}  {row.status:<12.12}  {name}")


def _filters(args: argparse.Namespace) -> dict[str, object]:
    return {
        "name": args.name,
        "user": args.user,
        "min_cpu": args.min_cpu,
        "min_memory": args.min_memory,
        "sort_by": args.sort,
        "limit": args.limit,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="process-watch", description="Inspect and monitor local processes safely.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} — Radwan Abdulhadi Ahmed (@rad03i2)")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--name", help="case-insensitive process-name substring")
        p.add_argument("--user", help="case-insensitive username substring")
        p.add_argument("--min-cpu", type=float, default=0.0, help="minimum CPU percentage")
        p.add_argument("--min-memory", type=float, default=0.0, help="minimum memory percentage")
        p.add_argument("--sort", choices=["cpu", "memory", "pid", "name"], default="cpu")
        p.add_argument("--limit", type=int, default=20, help="maximum rows (1-1000)")
        p.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    snapshot = sub.add_parser("snapshot", help="print one process snapshot")
    common(snapshot)

    watch = sub.add_parser("watch", help="print repeated process snapshots")
    common(watch)
    watch.add_argument("--interval", type=float, default=2.0, help="seconds between snapshots (0.2-3600)")
    watch.add_argument("--count", type=int, help="stop after this many snapshots")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            rows = collect_processes(**_filters(args))
            if args.json:
                print(json.dumps([row.to_dict() for row in rows], ensure_ascii=False, indent=2))
            else:
                _print_table(rows)
            return 0

        for index, rows in enumerate(watch_processes(interval=args.interval, count=args.count, **_filters(args)), start=1):
            if args.json:
                print(json.dumps({"snapshot": index, "processes": [row.to_dict() for row in rows]}, ensure_ascii=False))
            else:
                if index > 1:
                    print()
                print(f"Snapshot {index}")
                _print_table(rows)
        return 0
    except ValueError as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        print("\nMonitoring stopped.", file=sys.stderr)
        return 130
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
