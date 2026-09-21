from process_watch.cli import _bytes, build_parser


def test_human_bytes():
    assert _bytes(1024) == "1.0 KiB"
    assert _bytes(1024 * 1024) == "1.0 MiB"


def test_snapshot_parser_defaults():
    args = build_parser().parse_args(["snapshot"])
    assert args.command == "snapshot"
    assert args.limit == 20
    assert args.sort == "cpu"


def test_watch_parser_options():
    args = build_parser().parse_args(["watch", "--interval", "1", "--count", "3", "--name", "python", "--json"])
    assert args.interval == 1
    assert args.count == 3
    assert args.name == "python"
    assert args.json is True
