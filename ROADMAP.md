Roadmap

This roadmap groups planned improvements into milestones that build toward a stable 1.0. Items are prioritized for impact and safety. Timelines are indicative and can shift based on feedback.

## Milestone v0.1 – Core Reliability & DX

- Idempotency Keys: Add `idempotency_key` on `EventModel` (unique per `type`) to prevent duplicate events; helpers in generators.
- Scheduling & Priority: Add `not_before` (datetime) and `priority` (int); process respects both.
- Retries: Add `attempts`, `max_attempts`, `last_error_at`; separate “processed” from “exhausted”. Commands to requeue and to set max attempts.
- CLI Enhancements: `process_events` flags: `--types`, `--model`, `--limit`, `--batch-size`, `--once`, `--older-than`, `--only-errors`, `--max-attempts`, `--requeue-errors`.
- Structured Logging: Include event id, type, attempts, correlation id in log context.
- Signals: Emit `event_processed` and `event_failed` with context.
- Docs: Recipes for idempotency, retries, and on-commit event creation.

Acceptance
- Tests cover duplicate prevention, delayed processing, retries, and CLI options.
- Backward-compatible defaults; no migrations forced unless users opt-in to the extended model mixin.

## Milestone v0.2 – Observability, Admin, and Ops

- Metrics Hooks: Optional Prometheus/StatsD counters and durations (opt-in).
- Admin Mixin: Filters for `processed`, `error`, `type`, `date`; actions: Requeue, Mark processed.
- Retention & Health: Commands to purge/archive old processed events and detect “stuck” events.
- Requeue & Dead-letter: Simple requeue flow; optional dead-letter flag/collection.
- Correlation IDs: Field + helpers to propagate trace/correlation ids.

Acceptance
- Example admin integration and dashboards documented; metrics can be toggled via settings.

## Milestone v0.3 – Integrations & Async

- Pluggable Backends: Abstraction layer for dispatch; DB backend remains default. Optional Celery/RQ adapters without changing handler API.
- Async Handlers: Allow `async def` handlers; run via `async_to_sync` in the DB backend; native in async adapters.
- Batch Handlers: `@register(..., batch=True)` with bulk handler signature.

Acceptance
- Integration examples for Celery/RQ; CI exercises adapters at least with smoke tests.

## Milestone v0.4 – Performance & Safety

- Indexes: Recommend/add `Index` on `(processed, type)`, `(error, date)`, and `date`.
- Chunked Processing: Stable ordering; process in chunks (configurable); consistent `skip_locked` usage.
- Rate Limiting: Per-type throughput limits (token bucket / simple sleep-based throttle).
- Lock/Timeout Settings: Configurable lock timeout and polling interval.

Acceptance
- Benchmarks on a sample dataset; guidance in docs for tuning.

## Milestone v0.5 – DX & Ergonomics

- Signal Auto-wiring: Optional setting to auto-create events from model signals (create/update/delete) via a simple mapping config.
- Handler Filters: Decorator `when=` predicate for conditional execution.
- Strong Typing: `py.typed`, type hints, and `Protocol` for handler signatures.
- Exceptions: `EventProcessingError` with `code` and `retryable` semantics.
- Settings Namespace: `EVENTS_FRAMEWORK = {...}` for all tunables.

Acceptance
- mypy basic pass for the public API; examples use strong types.

## Compatibility & Testing

- Django Versions: Keep matrix for 3.2, 4.2; add 5.x; plan deprecation of 2.2.
- Python Versions: Maintain support for 3.8–3.11; add 3.12 when available.
- Concurrency Tests: Add tests for multi-worker processing and `skip_locked` behavior.
- Property/Stress Tests: Validate idempotency and retry invariants.

## Documentation

- Patterns & Recipes: On-commit events, retries, idempotency keys, batch processing, Celery integration, admin operations.
- Troubleshooting: Locking pitfalls, JSONField quirks, requeue strategies, dead-letter handling.
- Example Project: Demo app with multiple handlers, retries, metrics, and admin actions.

## Tracking & Process

- Issues: Track each roadmap item as a dedicated GitHub issue with label `roadmap` and milestone tags `v0.1` … `v0.5`.
- RFCs: For breaking or cross-cutting changes (e.g., plugin backend), add short RFCs in `docs/rfcs/` and link from issues.
- Release Cadence: Aim for small, incremental releases; update CHANGELOG per release and maintain upgrade notes.

