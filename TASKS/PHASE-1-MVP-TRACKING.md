# Phase 1 — MVP: Ride Tracking

Gate to enter: Phase 0 exit checklist (all `T0-*` `DONE`). May run in parallel with Phase 2 once Phase 0 is done — see `TASKS/README.md` § The Phase Rule.

---

### T1-01 — Location sampling module (Android + iOS)

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-09 |
| **Docs refs** | `docs/13-GPS/01-LOCATION-SAMPLING.md` |
| **Surface** | android, ios |

**Goal** — a module that emits GPS fixes per the sampling strategy (3s interval or 10m movement, accuracy ≤20m) and tags low-confidence points.

**Definition of Done**
- [ ] Emits points at the documented interval/distance thresholds
- [ ] Points with accuracy >20m tagged `low_confidence = true`, not dropped
- [ ] "Sinyal GPS lemah" UI signal fires after 60s with no valid fix

**Edge cases to test**
- [ ] No GPS fix at all for >60s → UI indicator shown, recording continues (not paused)
- [ ] Rapid movement (>10m within interval) triggers an early sample

---

### T1-02 — Local point buffer with periodic disk write

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-01 |
| **Docs refs** | `docs/16-RIDE/02-RIDE-RECORDING.md` § Resilience |
| **Surface** | android, ios |

**Definition of Done**
- [ ] Points buffered in memory, flushed to local DB every ~10s
- [ ] App force-killed mid-ride → points up to last flush are recoverable on relaunch

---

### T1-03 — RecordingService (foreground/background)

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-02 |
| **Docs refs** | `docs/01-PRD/04-RIDE-RECORDING.md`, `docs/16-RIDE/02-RIDE-RECORDING.md` |
| **Surface** | android, ios |

**Goal** — recording survives screen lock and app backgrounding for multi-hour rides.

**Definition of Done**
- [ ] Android: foreground service with persistent notification
- [ ] iOS: background location mode configured correctly
- [ ] Manual test: screen locked for 30+ min, recording continues uninterrupted

---

### T1-04 — Ride lifecycle state machine

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-07, T1-03 |
| **Docs refs** | `docs/16-RIDE/00-RIDE-LIFECYCLE.md` |
| **Surface** | backend, android, ios |

**Goal** — `recording → paused → recording → completed` (and `discarded`) transitions enforced identically on client and server; illegal transitions rejected.

**Definition of Done**
- [ ] All transitions in the state diagram implemented
- [ ] Illegal transitions (e.g. `completed → recording`) rejected server-side
- [ ] `is_short_ride` flag set correctly (<500m or <2min)

**Edge cases to test**
- [ ] Stop while still `paused` → riding_time excludes final open pause window
- [ ] Discard mid-recording → not present in history, not counted in stats

---

### T1-05 — Pause/resume and riding-time calculation

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-04 |
| **Docs refs** | `docs/13-GPS/09-PAUSE-RESUME.md` |
| **Surface** | backend |

**Definition of Done**
- [ ] `RidePauseEvent` created/closed correctly on pause/resume
- [ ] `riding_time_sec` formula matches the doc exactly, including the "stop while paused" edge case

**Edge cases to test**
- [ ] Multiple pause/resume cycles in one ride sum correctly
- [ ] Auto-pause prompt appears after 3 min under 2km/h, requires explicit confirm

---

### T1-06 — Batch GPS point upload endpoint

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-08, T0-11, T1-04 |
| **Docs refs** | `docs/13-GPS/00-GPS-ARCHITECTURE.md`, `backend/docs/CODING_STANDARDS.md` §9 |
| **Surface** | backend |

**Definition of Done**
- [ ] Endpoint accepts a batch of points for a `completed` ride
- [ ] Retried safely on upload failure (idempotent — re-upload of the same batch doesn't duplicate points)
- [ ] Raw points written through `StorageDriver` under a `private/` key (not to Postgres, not via `fs` directly); `Track.raw_points_ref` stores the key

---

### T1-07 — Polyline simplify + encode job

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-06 |
| **Docs refs** | `docs/13-GPS/00-GPS-ARCHITECTURE.md` |
| **Surface** | backend |

**Definition of Done**
- [ ] Track.polyline populated using Google Polyline Algorithm encoding
- [ ] `point_count` recorded

---

### T1-08 — Distance calculation

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-06 |
| **Docs refs** | `docs/13-GPS/07-DISTANCE-CALCULATION.md` |
| **Surface** | backend |

**Definition of Done**
- [ ] Haversine accumulation across valid points only
- [ ] `low_confidence` points skipped (not treated as zero-distance)
- [ ] GPS jump (>500m in <3s) retroactively flagged `low_confidence` and excluded

**Edge cases to test**
- [ ] Synthetic GPS jump in test fixture does not inflate `distance_km`
- [ ] All-low-confidence ride (GPS failure throughout) → distance computed as 0, not an error

---

### T1-09 — Speed calculation

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-08 |
| **Docs refs** | `docs/13-GPS/06-SPEED-CALCULATION.md` |
| **Surface** | backend |

**Definition of Done**
- [ ] `avg_speed_kmh = distance_km / (riding_time_sec/3600)`
- [ ] `max_speed_kmh` excludes readings >220 km/h
- [ ] 220 km/h threshold is a named constant, not a magic number

---

### T1-10 — Ride completion pipeline

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-07, T1-08, T1-09 |
| **Docs refs** | `docs/01-PRD/06-RIDE-ANALYTICS.md`, `docs/07-DOMAIN/01-RIDER.md` |
| **Surface** | backend |

**Goal** — on `stop`, compute all summary metrics once and update `Rider` aggregate stats incrementally, race-condition-safe.

**Definition of Done**
- [ ] All `Ride` summary columns populated exactly once per completion
- [ ] `Rider.total_distance_km`/`total_rides`/`total_duration_min` updated incrementally, not via full recompute
- [ ] Double-completion (retry) does not double-count stats (see `MEMORY/ARCHITECTURE-NOTES.md`)

**Edge cases to test**
- [ ] Concurrent duplicate `stop` calls for the same ride → stats incremented once

---

### T1-11 — Ride history endpoints + UI

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-10 |
| **Docs refs** | `docs/01-PRD/05-RIDE-HISTORY.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Paginated list endpoint, newest first
- [ ] Detail endpoint returns full metrics + polyline
- [ ] Mobile list + detail screens implemented

---

### T1-12 — Edit / soft-delete ride

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-11 |
| **Docs refs** | `docs/01-PRD/05-RIDE-HISTORY.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Title/visibility editable after completion
- [ ] Soft-delete with 30-day retention before an idempotent hard-delete job removes raw points via `StorageDriver.delete()`
- [ ] Visibility change to private hides any associated `Post` from feed (coordinate with `T2-06`)

---

### T1-13 — Mobile recording UI

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-04, T1-05 |
| **Docs refs** | `docs/01-PRD/04-RIDE-RECORDING.md` |
| **Surface** | android, ios |

**Definition of Done**
- [ ] Start/pause/resume/stop controls
- [ ] Live jarak & durasi kasar shown during recording
- [ ] Post-stop summary screen (map + metrics)

---

### T1-14 — Crash-recovery flow

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-02, T1-13 |
| **Docs refs** | `docs/16-RIDE/02-RIDE-RECORDING.md` § Resilience |
| **Surface** | android, ios |

**Definition of Done**
- [ ] App relaunch after crash/kill during `recording` offers resume/finish/discard using locally buffered data
- [ ] No silent data loss for points already flushed to local disk
