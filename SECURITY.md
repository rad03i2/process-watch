# Security Policy

## Scope

Process Watch reads operating-system process metadata exposed to the current user through `psutil`. It does not send telemetry, contact remote services, terminate processes, change priorities, inject code, or require credentials.

## Privacy

Process names and usernames can be sensitive on shared systems. JSON or terminal output should be treated as local diagnostic data. Review it before posting publicly.

## Privileges

Run with normal user privileges. Elevated privileges may reveal additional process metadata and are not required for normal use. Inaccessible processes are skipped rather than causing the scan to fail.

## Reporting vulnerabilities

Please use GitHub's private vulnerability reporting feature for this repository when available. Do not publish exploitable details before a fix can be prepared.

## Supported versions

Security fixes target the latest release on the `main` branch.
