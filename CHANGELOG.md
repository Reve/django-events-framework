Changelog

This project adheres to Keep a Changelog principles and aims to follow SemVer once stable.

## [0.0.15]

Date: 2026-10-20

Added
- `RetryEvent` leaves an event pending for the next processing run without adding model fields or migrations. Ordinary exceptions retain terminal error handling.

Fixed
- Roll back handler database changes before recording a failure, including database errors that would otherwise leave the transaction unusable.
- Clear error fields after a successful retry.

## [0.0.14]

Date: 2025-09-05

Added
- GitHub Actions CI matrix for Django (2.2, 3.2, 4.2) across Python (3.8–3.11).
- GitHub Actions publish workflow for TestPyPI on tags (v*).
- Quickstart and Concurrency & Error Handling sections in README.
- RELEASE.md with step-by-step publishing guide.

Changed
- Packaging moved to setup.cfg as the single source of truth; setup.py now defers to setup.cfg.
- Requirements aligned with code (use `jsonfield` for Django 2.x) and clarified Python/Django support in classifiers.
- Events registry structure supports multiple handlers per (EventModel, type).
- `as_choices` preserves declared values and human-readable labels.
- Library logging cleaned up (no basicConfig); improved autodiscovery error reporting.
- Removed non-standard `default = True` from AppConfig.

Fixed
- N/A

Notes
- Historical releases prior to 0.0.14 were not documented in this changelog.

