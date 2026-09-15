# Phase 2 — MVP: Social Media Share

Gate to enter: Phase 0 exit checklist (all `T0-*` `DONE`). May run in parallel with Phase 1 — see `TASKS/README.md` § The Phase Rule. `T2-06` onward additionally depends on Phase 1's ride-completion pipeline (`T1-10`) since a post wraps a completed ride.

---

### T2-01 — Register / login (email + password)

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T0-08 |
| **Docs refs** | `docs/01-PRD/01-AUTHENTICATION.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Register: unique email/username enforced, password ≥8 chars, bcrypt/argon2 hashed
- [ ] Login: rate-limited (5 failed attempts / 15 min / account)
- [ ] Mobile register/login screens

**Edge cases to test**
- [ ] 6th failed login attempt within 15 min rejected regardless of correctness
- [ ] Duplicate email/username (case-insensitive) rejected

---

### T2-02 — OAuth Google

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-01 |
| **Docs refs** | `docs/01-PRD/01-AUTHENTICATION.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] New account auto-created from Google profile on first login
- [ ] Email from Google treated as pre-verified
- [ ] `oauth_provider` set correctly; `password_hash` remains nullable for these accounts

---

### T2-03 — Reset password

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-01 |
| **Docs refs** | `docs/01-PRD/01-AUTHENTICATION.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Reset link/code expires in 30 min
- [ ] Old sessions unaffected unless explicitly revoked

---

### T2-04 — Rider profile CRUD + stats display

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-01 |
| **Docs refs** | `docs/01-PRD/02-RIDER-PROFILE.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Edit name/avatar/bio
- [ ] Public profile shows only `public` rides; own profile stats include private rides
- [ ] Username change rate-limited to once/30 days

---

### T2-05 — Follow / unfollow

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-04 |
| **Docs refs** | `docs/24-SOCIAL/00-SOCIAL-GRAPH.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Follow/unfollow instant, no approval
- [ ] Self-follow rejected (defense in depth on top of `T0-07`'s DB constraint)
- [ ] Follower/following lists with quick follow/unfollow toggle

---

### T2-06 — Publish / unpublish ride

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-10, T2-04 |
| **Docs refs** | `docs/24-SOCIAL/08-RIDE-POST.md`, `docs/16-RIDE/08-RIDE-SHARING.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Publish creates `Post`, sets `Ride.visibility = public` if it wasn't already
- [ ] Unpublish soft-deletes `Post`; does **not** revert `Ride.visibility`
- [ ] Post data (metrics) reflects live `Ride` state, not a snapshot; caption is independently editable

---

### T2-07 — Feed endpoint + UI

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-05, T2-06 |
| **Docs refs** | `docs/24-SOCIAL/03-FEED.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Fan-out-on-read query per the doc, paginated (20/page)
- [ ] Own posts included alongside followees'
- [ ] Pull-to-refresh + infinite scroll UI

---

### T2-08 — Kudos

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-06 |
| **Docs refs** | `docs/01-PRD/15-COMMENTS-KUDOS.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Toggle on/off, one kudos per rider per post enforced at DB level (`T0-07`)
- [ ] Count shown on post card

---

### T2-09 — Comments

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-06 |
| **Docs refs** | `docs/01-PRD/15-COMMENTS-KUDOS.md` |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Create (≤500 chars), soft-delete by author or post owner
- [ ] Chronological, non-threaded

---

### T2-10 — In-app notifications

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-05, T2-08, T2-09 |
| **Docs refs** | `docs/01-PRD/15-COMMENTS-KUDOS.md` § Notifikasi |
| **Surface** | backend, android, ios |

**Definition of Done**
- [ ] Notification created on new kudos, new comment, new follower
- [ ] Badge count + list UI (in-app only, no push in MVP)

---

### T2-11 — Share card rendering

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T1-10 |
| **Docs refs** | `docs/24-SOCIAL/09-SHARE-CARD.md` |
| **Surface** | android, ios |

**Definition of Done**
- [ ] Client-side render: map + judul + jarak/durasi/kecepatan rata-rata + avatar + watermark
- [ ] 1:1 variant shipped (Story 9:16 optional, not required for MVP exit)
- [ ] Rendered image cached, not regenerated on every open unless ride data changed

---

### T2-12 — Native share sheet integration

| | |
|---|---|
| **Status** | TODO |
| **Depends on** | T2-11 |
| **Docs refs** | `docs/24-SOCIAL/09-SHARE-CARD.md`, `docs/16-RIDE/08-RIDE-SHARING.md` |
| **Surface** | android, ios |

**Definition of Done**
- [ ] OS native share sheet invoked with the rendered share card image
- [ ] Works for both `public` and `private` rides (share-out does not require publish)
