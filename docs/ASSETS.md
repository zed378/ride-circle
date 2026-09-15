# Asset Sources & Licensing

Required by `TASKS/specs/T3-02-landing-page.md` §24. One row per external image used anywhere in `web/`. **An asset is not used in the codebase until it has a row here** — this file is filled in as part of implementing `T3-02`, not written retroactively.

Never use an asset with an ambiguous or unverifiable license, per the spec's §24 "Never use an asset if its licensing status is ambiguous."

## Landing page images

| Local filename | Source platform | Original URL | Author/contributor | Date retrieved | License | Attribution required? | Section used | Rights concerns checked |
|---|---|---|---|---|---|---|---|---|
| `landing-hero.webp` | | | | | | | Hero (§9) | Logos / plates / recognizable people / branded gear — none present |
| `landing-story-route.webp` | | | | | | | Story section (§12) | |
| `landing-ride.webp` | | | | | | | Ride Recording section (§13) | |
| `landing-route.webp` | | | | | | | Route Discovery section (§14) | |
| `landing-group.webp` | | | | | | | Group Ride section (§15) | |
| `landing-garage.webp` | | | | | | | Motorcycle Identity section (§16) | |
| `landing-safety.webp` | | | | | | | Safety section (§17) | |
| `landing-community.webp` | | | | | | | Community section (§18) | |
| `landing-final.webp` | | | | | | | Final CTA (§22) | |

## Checklist before an asset row is considered complete

Per `TASKS/specs/T3-02-landing-page.md` §24, every row above must be verified against all of:

- [ ] Sourced from Pexels, Unsplash, or Pixabay only (in that priority order)
- [ ] No visible motorcycle manufacturer, helmet, or apparel logos
- [ ] No visible license plates
- [ ] No identifiable private property
- [ ] No recognizable people in a way that implies endorsement
- [ ] Downloaded and stored locally in `public/images/landing/` — never hotlinked in production
- [ ] Converted to WebP (or AVIF)
- [ ] License terms permit commercial use on a public website

## Brand assets

Logo, favicon, and other first-party brand assets are not third-party sourced and don't need a row here — track them separately if a brand asset audit is ever needed.
