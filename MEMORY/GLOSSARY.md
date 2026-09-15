# Glossary

Domain terms specific to RideCircle. Not part of the base `TASKS`/`MEMORY` convention this repo follows — added because motorcycle-domain vocabulary and this project's specific renaming choices aren't obvious from general knowledge or from the convention itself.

| Term | Meaning in this project |
|---|---|
| **Ride** | One recorded riding session, start to stop. Central entity of the Tracking pillar. Named "Ride" rather than "Activity" deliberately — see `docs/07-DOMAIN/03-RIDE.md`. |
| **Rider** | A user of the app. Not "athlete." |
| **Post** | The public, in-feed representation of a published `Ride`. One `Ride` ↔ at most one `Post`. |
| **Share Card** | An image generated from a ride for sharing *outside* the app (WhatsApp/Instagram) — distinct from `Post`, which is *inside* the app. |
| **Kudos** | The like/appreciation action on a `Post`. Term kept from Strava-style tracking apps since it's already familiar to the target audience. |
| **Riding time** | Ride duration minus paused time. Different from `duration`, which includes pauses. |
| **Track** | The raw/encoded GPS data of a ride (polyline + raw points), a separate entity from `Ride` for storage reasons (raw points live in file storage — driver-agnostic, local disk by default, ADR-011 — not the relational database). |
| **Low confidence point** | A GPS fix with accuracy worse than 20m — stored, but excluded from distance/speed calculations. |
| **Fan-out-on-read / fan-out-on-write** | Two feed-generation strategies. MVP uses fan-out-on-read (`ADR-005`). |
| **Moto Club** *(Post-MVP)* | A first-class entity for motorcycle clubs — not a generic "group." Will have roles, rules, verification. |
| **Group Ride** *(Post-MVP)* | A jointly-tracked riding session with leader/sweeper/roster — not just several riders separately posting the same ride. |
| **Sweeper** *(Post-MVP, community term)* | The rider positioned at the back of a group ride, responsible for making sure nobody is left behind. |
| **Segment** *(Post-MVP)* | A comparable portion of a route (Strava-style). Deliberately Post-MVP — see the safety rationale in `docs/17-RIDER-PERFORMANCE/00-PERFORMANCE-MODEL.md`. |
| **Garage** *(Post-MVP)* | A rider's collection of owned motorcycles, with service/modification history. |
