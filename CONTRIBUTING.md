# Contributing

Thanks for improving Process Watch.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and create a virtual environment.
3. Install development dependencies with `python -m pip install -e ".[dev]"`.
4. Keep process collection read-only and cross-platform; do not add process-killing or privilege-escalation behavior to unrelated changes.
5. Add or update tests for behavior changes.
6. Run `python -m compileall -q src tests` and `python -m pytest` before opening a pull request.
7. Update both English and Arabic README sections when user-facing behavior changes.

Please keep commits focused and never include credentials, local process dumps, personal usernames, generated environments, or machine-specific files.
