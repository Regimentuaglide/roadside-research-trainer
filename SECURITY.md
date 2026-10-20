# Security Policy — Roadside Research Trainer

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.9.x   | ✅        |
| < 0.9   | ❌        |

## Reporting a Vulnerability

Roadside Research Trainer runs with elevated screen-capture privileges. If you discover a vulnerability (privilege escalation, arbitrary file write via export path, unsafe deserialization of session files, etc.), please do **not** open a public issue.

Email: security@roadside-research-trainer.dev (PGP key on request).

We aim to acknowledge within 72 hours and provide a fix within 14 days for confirmed issues.

## Scope

In scope:
- `rrt/core/` (route engine, capture pipeline)
- `rrt/services/export_service.py` (path handling, serialization)
- `rrt/handlers/` (input handlers, hotkey registration)

Out of scope:
- Third-party game clients or anti-cheat systems.
- User-supplied route files loaded from untrusted sources.

## Hardening Notes

- Session files are JSON; loading uses `json.load` with a size cap (see `rrt/utils/paths.py`).
- The overlay uses Win32 layered windows — do not disable `WS_EX_NOACTIVATE`.
- Capture is restricted to the primary monitor unless the user opts in.

**Use at your own risk.** Roadside Research Trainer is provided for educational field-research purposes only. The authors are not responsible for misuse or for violations of any platform's terms of service.