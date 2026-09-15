# Architecture Notes (informal)

Technical notes not yet mature enough for `docs/08-ARCHITECTURE/` or a formal ADR in `DECISIONS.md`. Promote to one of those once matured/decided; don't let this file become a dumping ground that never gets resolved.

## Ideas raised during scaffolding, not yet decided

- **PostGIS from day one?** MVP doesn't strictly need geospatial queries (no "find rides near this point"), but enabling the PostGIS extension now avoids a painful migration once Route Discovery (roadmap Fase 4) needs real geospatial querying. Leaning: yes, enable at `T0-05` even though unused until later.
- **Polyline encoding** — use the standard Google Polyline Algorithm, not a custom format, for compatibility with off-the-shelf map rendering libraries.
- **Static map thumbnails for feed cards** — generate and cache at ride-completion time (`T1-10`), not on-the-fly per feed request. Expensive and slow to regenerate per view.

## Performance questions not yet relevant at MVP scale, noted for later

- Fan-out-on-read (ADR-005) degrades as a rider's following count grows into the thousands. Not a real problem at MVP scale; revisit if/when it becomes one.
- `Rider` aggregate stats (`total_distance_km` etc.) are updated incrementally on ride completion (`T1-10`) — needs to be provably idempotent against retries/duplicate completion calls, or stats will drift over time. Flagged as an explicit edge case on `T1-10`.
