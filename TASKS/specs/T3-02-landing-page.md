# Spec — T3-02 / T3-03: Landing Page

**Task:** `TASKS/PHASE-3-WEB.md` § T3-02 (Landing page sections), T3-03 (SEO & performance)
**Spec required:** Yes — this document, per `TASKS/00-TASK-CONVENTIONS.md` § Definition of Ready
**Status:** Ready — reconciliation resolved 2026-09-15 (see below and `MEMORY/DECISIONS.md` ADR-009); `T3-02` unblocked
**Source:** Pasted by the user as a `claude -p` execution prompt on 2026-09-15. Stored here as the authoritative spec for T3-02/T3-03 rather than executed directly, so it goes through the same `docs/` cross-referencing and MEMORY discipline as every other task in this repo.

---

## Reconciliation notes (read this before implementing)

This spec was written as a **standalone, self-contained brief** — it doesn't reference `docs/01-PRD/22-LANDING-PAGE.md`, `web/docs/CODING_STANDARDS.md`, or any other file in this repo, because it was authored outside this project's planning system. Two things need reconciling before an agent executes it:

1. **Product name — RESOLVED 2026-09-15.** This spec calls the product **RIDELINE** throughout (wordmark, footer copyright, hero UI card, page title, meta description). The rest of this repo calls it **RideCircle**. **Decision: keep RideCircle.** See `MEMORY/DECISIONS.md` ADR-009. A substitution table is at the bottom of this document (§ Product name substitutions) — every literal "RIDELINE" below stays as originally pasted (this spec is preserved verbatim as received), but implementation must use "RideCircle" at each of the six locations listed there.
2. **Tech stack match.** The spec's §43 ("Technical Implementation") tells the executing agent to inspect the repo and use whatever frontend stack already exists. That stack is already decided in this repo: Next.js (App Router), React, TypeScript, Tailwind CSS, Zustand — see `web/docs/CODING_STANDARDS.md` and `MEMORY/DECISIONS.md` ADR-008. Sections §27 (Component System) and §44–45 (Content/Asset Architecture) below should be implemented following that document's conventions (component naming, `src/components/landing/` placement, `api/services/` layering where the page needs any dynamic data) — this spec's own naming (e.g. `LandingPage`, `HeroSection`) is compatible with `web/docs/CODING_STANDARDS.md` §3's structure and needs no translation.

Everything else below is precise enough (exact copy, exact hex colors, exact section order, exact motion timings) that it should be treated as binding, not as inspiration — that precision is the point of the brief, per its own §50 "Execution Mode."

## How this spec relates to `docs/01-PRD/22-LANDING-PAGE.md`

`docs/01-PRD/22-LANDING-PAGE.md` states the **product requirement** (why a landing page exists, what it must achieve for MVP, what's explicitly out of scope). This document is the **design/implementation brief** for that requirement — much more detailed than the PRD needs to be, because a PRD documents intent and this documents execution precisely enough for an agent to build from directly. Where the two overlap (e.g. "download buttons link to store listings"), they agree; nothing here contradicts the PRD's scope boundaries (no blog, no dynamic waitlist system, etc. — this spec's sections stay within what §6 "Page Structure" lists, which matches the PRD's MVP scope).

## Verbatim specification

The section below is preserved close to verbatim from what the user provided (only the outer `claude -p "$(cat <<'PROMPT' ... PROMPT)"` shell-invocation wrapper was removed, and the `====` ASCII section dividers were converted to markdown headers — no wording, values, or requirements were changed).

---

You are acting as a Principal Product Designer, Senior UI/UX Designer, Brand Designer, Senior Frontend Engineer, Motion Designer, and Conversion-focused Product Strategist.

You are working inside an existing web application repository.

YOUR TASK
=========
Design and implement the complete PUBLIC LANDING PAGE for a motorcycle-focused social fitness / riding platform inspired by the product mechanics of Strava, but explicitly redesigned for motorcycle riders.

This is NOT a generic "Strava clone".
This is NOT a generic motorcycle website.
This is NOT an AI-looking SaaS landing page.

The product positioning is:

"A social riding platform for people who ride motorcycles — discover routes, record rides, ride with friends, build your riding identity, and stay connected and safer on the road."

The product must feel like a real motorcycle product built by people who actually understand motorcycle culture, long-distance touring, weekend rides, riding groups, routes, fuel stops, destinations, motorcycle ownership, and rider communities.

IMPORTANT:
Do not ask me any design, product, copywriting, layout, color, typography, asset, animation, content, or UX questions.
All decisions have already been made in this specification.
When something is not explicitly stated, use the nearest existing rule in this specification and make a sensible implementation decision.
Do not stop for clarification.
Do not create an "Open Questions" section.
Do not leave placeholders such as "Lorem ipsum", "Coming soon", "TBD", "Your text here", "Image here", or "Feature title".
Do not invent fake customer logos, fake companies, fake statistics, fake testimonials, fake awards, or fake partnerships.

## 1. PRODUCT CONCEPT

Working product name:
RIDELINE

Brand promise:
"Your rides. Your routes. Your people."

Primary audience:
- motorcycle riders
- weekend riders
- touring riders
- urban riders
- motorcycle communities
- small and large riding groups
- riders who enjoy route discovery
- riders who care about riding history and motorcycle ownership
- riders who want group-ride coordination and safety

Secondary audience:
- moto clubs
- motorcycle event organizers
- motorcycle brands
- dealerships
- workshops
- riding gear brands
- route destinations
- motorcycle communities

Primary product pillars:
1. Record every ride
2. Discover better routes
3. Ride together
4. Build your rider identity
5. Track your motorcycle
6. Stay connected and safer
7. Join the motorcycle community

Do not frame the product primarily as:
- a racing application
- a speed competition application
- a generic GPS tracker
- a motorcycle marketplace
- a navigation replacement

Navigation and GPS are capabilities.
Community and riding identity are the product.

## 2. LANDING PAGE OBJECTIVE

Primary conversion:
Create account / Start riding

Secondary conversion:
Explore the product

Tertiary conversion:
Explore community / routes / group rides

The landing page must communicate within the first 5 seconds:

WHAT:
A social platform built specifically for motorcycle riders.

WHY:
Riding becomes better when your routes, rides, friends, motorcycle, and community live in one place.

HOW:
Record → Discover → Ride → Share → Connect.

The page should feel:
- premium
- mature
- editorial
- adventurous
- technical
- authentic
- confident
- human
- understated
- cinematic
- contemporary

Avoid:
- gamer aesthetics
- cyberpunk
- excessive neon
- fake futuristic dashboards
- cliché speedometer graphics
- generic AI gradients
- excessive glassmorphism
- purple/blue SaaS gradients
- over-rounded UI
- giant meaningless 3D motorcycles
- stock-photo collage
- emoji-heavy design
- childish motorcycle imagery
- overused dark-mode "developer landing page" aesthetic

## 3. BRAND CHARACTER

Brand personality:

CONFIDENT
Not loud.

ADVENTUROUS
Not reckless.

TECHNICAL
Not robotic.

SOCIAL
Not childish.

PREMIUM
Not luxurious for the sake of luxury.

MOTORCYCLE-CULTURE-AWARE
Not stereotypical.

The visual language should feel closer to:
- premium automotive editorial
- contemporary outdoor equipment brands
- modern mobility products
- high-end motorcycle magazines
- modern mapping products

than:
- gaming
- crypto
- generic SaaS
- startup template websites.

## 4. CORE VISUAL DIRECTION

Use a predominantly dark visual system.

Primary background:
#0B0C0D

Secondary background:
#111315

Surface:
#17191C

Elevated surface:
#1D2024

Primary text:
#F3F3EF

Secondary text:
#A5A8AA

Muted text:
#70757A

Primary accent:
#D8FF3E

Accent should be used sparingly for:
- CTA
- active navigation
- map route
- important metric
- selected state
- tiny visual highlight

Supporting accent:
#FF6B35

Use supporting orange only in tiny quantities for:
- warning/road/safety contextual accent
- activity heat
- occasional editorial detail

Do NOT use:
- purple gradients
- cyan gradients
- pink gradients
- rainbow gradients
- excessive pure white
- excessive lime backgrounds

Do not make every section black.
Create subtle tonal differences between sections.

Color hierarchy:
Background → Surface → Elevated Surface → Border → Text → Accent.

Borders:
rgba(255,255,255,0.08)

Dividers:
rgba(255,255,255,0.06)

Do not use heavy shadows.
Prefer contrast, borders, depth, image treatment, and spacing.

## 5. TYPOGRAPHY

Use a modern grotesk / neo-grotesk type system.

Preferred:
Inter,
Manrope,
Geist,
or an equivalent modern sans-serif already present in the repository.

If the repository already has a brand font, preserve it unless it violates the aesthetic.

Typography hierarchy:

H1:
large, compact, bold,
responsive clamp,
approximately 64–88px desktop.

H2:
42–56px.

H3:
24–32px.

Body:
17–19px desktop,
16px mobile.

Small labels:
11–13px,
uppercase sparingly,
letter-spacing approximately 0.08em–0.12em.

Avoid:
- excessive italic display fonts
- futuristic fonts
- condensed racing fonts
- handwritten fonts
- decorative type

Typography should feel editorial and premium.

## 6. PAGE STRUCTURE

Implement exactly this landing-page architecture:

01. Announcement / Utility Bar
02. Main Navigation
03. Hero
04. Product Proof Strip
05. "Riding Is More Than Distance" Story Section
06. Ride Recording Experience
07. Route Discovery Experience
08. Group Ride Experience
09. Rider + Motorcycle Identity
10. Safety Experience
11. Community Experience
12. Performance / Riding History
13. Visual Route / Map Immersion Section
14. Social Proof / Community Signals
15. Final CTA
16. Footer

Do NOT add:
- generic FAQ section
- fake testimonials
- fake customer logos
- generic newsletter section
- generic "trusted by" section
- meaningless pricing table on the homepage
- excessive feature grids
unless an equivalent real feature already exists in the repository.

## 7. ANNOUNCEMENT BAR

Keep this minimal.

Copy:

"Built for riders, not spectators."

On the right:
"Join the ride →"

Small typography.

This section should not visually dominate.

## 8. MAIN NAVIGATION

Desktop navigation:

Logo:
RIDELINE

Navigation:
Rides
Routes
Clubs
Events

Right:
Log in
Start Riding

Navigation behavior:
- transparent over hero initially
- becomes slightly opaque after scroll
- backdrop blur only when necessary
- thin bottom border after scroll
- sticky
- mobile drawer with full-height premium layout

Logo treatment:
WORDMARK only in navigation.
Do not create fake iconography unless a real logo asset already exists.

## 9. HERO

The hero must be visually dominant.

Layout:
Full viewport / approximately 90vh.

Background:
A cinematic real-world motorcycle riding photograph.

Composition:
- rider or motorcycle should not sit directly beneath the headline
- image should provide negative space for typography
- road should lead the eye into the composition
- prefer mountains / coast / long road / curves / forest / open landscape
- avoid wheelies
- avoid reckless overtaking
- avoid obvious racing circuit imagery
- avoid visible commercial logos
- avoid giant recognizable motorcycle manufacturer logos
- avoid stock-photo "thumbs up" poses
- avoid fake-looking AI motorcycles

Hero visual treatment:
- dark gradient from left / bottom
- subtle grain
- subtle vignette
- no artificial cyber glow

Headline:

"Ride further.
Remember every mile."

Supporting copy:

"Record your rides, discover roads worth taking, and stay connected with the people who ride with you."

Primary CTA:
"Start Riding"

Secondary CTA:
"Explore the Platform"

Under CTA:
"No matter what you ride."

Do not use:
"Ride. Connect. Explore." as the main headline.
It is too generic.

Hero micro interaction:
On initial load:
- headline enters with controlled vertical reveal
- supporting copy follows
- buttons follow
- image has extremely subtle scale-in
- no excessive animation

After page load:
Hero image may have extremely subtle parallax, maximum 6–10px movement.
Nothing more.

## 10. HERO SUPPORTING VISUAL

Create a floating product UI overlay in the hero.

Do NOT use a fake generic SaaS dashboard.

Use a realistic riding activity card:

RIDELINE RIDE

"Malang → Batu → Pujon"

147.8 km
3h 42m
39.9 km/h avg
+1,462 m elevation

Map thumbnail:
Dark route map with a lime route line.

Bottom metadata:
"Sunday · 06:14"

The UI must look like a real mobile riding product.

Keep overlay compact.
Do not cover the entire photograph.

## 11. PRODUCT PROOF STRIP

Immediately after hero.

Use 4 compact statements:

"Every ride becomes part of your story."
"Routes shaped by riders."
"Built for group rides."
"Your motorcycle, your history."

Do NOT fabricate numeric claims.

No "1M riders".
No "50 countries".
No fake statistics.

## 12. STORY SECTION

Headline:

"Riding is more than distance."

Body:

"The road is the destination, the people make the story, and every ride leaves something worth keeping."

Then three editorial statements:

01
THE ROUTE
"Find roads worth taking."

02
THE RIDE
"Capture every turn, stop, climb, and detour."

03
THE PEOPLE
"Ride with your club, your friends, and your community."

Visual layout:
large image + typography,
not a generic three-column SaaS card grid.

Use asymmetry.

## 13. RIDE RECORDING SECTION

Section headline:

"Your ride, from ignition to finish."

Copy:

"Record the route, distance, elevation, riding time, stops, and the moments that made the ride memorable."

Visual:
Large phone mockup showing a ride recording screen.

UI content:
- distance
- moving time
- average speed
- elevation
- map
- current ride status

Secondary visual:
small route trace.

Interaction:
desktop:
- scrolling can transition the displayed UI state

mobile:
- no complicated scroll-jacking
- simple reveal sequence

Avoid showing top speed as a hero metric.
Do not glorify dangerous riding behavior.

## 14. ROUTE DISCOVERY SECTION

Headline:

"Stop taking the same road."

Copy:

"Discover routes shaped by riders who were already out there."

Show:
- route cards
- route difficulty
- distance
- elevation
- estimated riding time
- terrain / scenery tags
- scenic indicator
- fuel stop
- rest stop
- destination

Example cards:

"North Coast Run"
184 km · Moderate

"Mountain Loop"
126 km · Curvy · +1,840 m

"Sunrise Ridge"
92 km · Scenic

These are illustrative product UI labels, not claims about actual locations.

Visual:
Large dark map with glowing/subtle route traces.

Use:
- lime primary route
- muted grey secondary routes
- orange only for selected contextual markers

Do not use Google Maps screenshot assets.
Do not reproduce copyrighted third-party map UI.
Use a custom abstract map visual or the application's existing map component.

## 15. GROUP RIDE SECTION

THIS IS A MAJOR DIFFERENTIATOR.

Headline:

"Nobody gets left behind."

Copy:

"Plan the route, set the order, regroup at waypoints, and keep the whole crew on the same ride."

Show a realistic group ride interface.

Example:
GROUP RIDE
"Sunday East Java Loop"

Leader
Rider 01

8 riders
142 km planned

Waypoint:
"Coffee Stop · 72 km"

Status indicators:
7 riding
1 regrouping

Do not show dangerous rider positions.
Do not imply encouragement to speed.

Key visual:
A map showing 5–8 rider markers connected through a route.

Animate:
- route appears
- rider markers move subtly
- one rider temporarily becomes "regrouping"
- group state resolves

This animation must be slow, calm, and informative.

## 16. MOTORCYCLE IDENTITY SECTION

Headline:

"Your bike is part of the story."

Copy:

"Keep your motorcycle, mileage, modifications, service history, gear, and rides together."

Create a premium motorcycle profile card:

YAMAHA XSR 155
"Black / Custom"

18,420 km

Last service:
1,240 km ago

Rides:
86

Favorite route:
"Batu Loop"

IMPORTANT:
The motorcycle brand/model above is fictional UI data.
Do not present it as a real user's data.

Visual direction:
premium garage/editorial photography,
not dealership advertisement.

Include "Your Garage" mini interface.

## 17. SAFETY SECTION

Headline:

"Ride together. Stay connected."

Copy:

"When a group ride changes, your people should know. Keep important contacts, live ride status, and regroup points close at hand."

Visual:
Dark UI with:
- live group position
- last known location
- rider status
- regroup point
- emergency contact

Do not make medical or emergency-service promises.

Do not claim:
"Emergency response guaranteed."
"Accident detection saves lives."
unless an actual implemented service exists.

Use measured language.

CTA:
"See how group riding works"

## 18. COMMUNITY SECTION

Headline:

"The best roads are shared."

Copy:

"Follow riders, join clubs, discover events, give kudos, and build your place in the riding community."

Visual:
Editorial activity feed.

Example activity cards:

"Ardi completed Mountain Loop"
"126 km · 3h 14m"

"Sunday Riders Club"
"38 riders · Jakarta"

"Rizal shared a new route"
"South Coast Explorer · 208 km"

Keep names as fictional UI data.

Include:
- avatar circles
- motorcycle thumbnail
- route map
- kudos
- comments
- club badge

Avoid Instagram clone aesthetics.

This is a riding activity network, not a photo-first social network.

## 19. PERFORMANCE / RIDING HISTORY SECTION

Headline:

"Look back. Ride smarter."

Copy:

"Your riding history becomes a picture of how, where, and why you ride."

Visual:
Elegant analytics screen.

Metrics:
Monthly distance
Ride count
Average ride distance
Elevation
Favorite routes
Favorite riding days

Chart:
minimal line/bar chart

Do not overuse dashboards.

One chart.
Strong editorial composition.

## 20. MAP IMMERSION SECTION

This section should create visual memorability.

Full-width dark map composition.

Headline:

"Every road leaves a trace."

Overlay:
A route from starting point to destination.

Small labels:
Start
Fuel
Coffee
Viewpoint
Regroup

Use a very thin, precise visual system.

No rainbow heatmaps.

The map should feel like:
- cartography
- motorcycle touring
- modern navigation
- premium technical documentation

not:
- gaming minimap.

## 21. SOCIAL PROOF

No fake testimonials.

Instead use "community signals".

Example:

"Built around the way riders actually ride."

Show:
CLUBS
GROUP RIDES
ROUTES
RIDES
EVENTS

Do not show fake numerical totals.

If the actual backend has real metrics, use those.
Otherwise use category labels only.

## 22. FINAL CTA

Large section.

Headline:

"Your next ride starts here."

Supporting copy:

"Bring your bike. Bring your crew. Bring the road."

Primary CTA:
"Start Riding"

Secondary:
"Explore Routes"

Visual:
Wide cinematic motorcycle road image.

Composition:
road occupies lower half,
dark sky / negative space at top,
copy placed in negative space.

Animation:
slow image reveal,
button hover,
subtle grain.

## 23. FOOTER

Footer content:

RIDELINE

"Your rides. Your routes. Your people."

Columns:

PRODUCT
Rides
Routes
Clubs
Events

COMMUNITY
Moto Clubs
Group Rides
Challenges

COMPANY
About
Contact

LEGAL
Privacy
Terms
Cookies

SOCIAL
Instagram
YouTube
Community

Bottom:
© current year RIDELINE

Do not create fake social URLs.
Use "#" only if no actual links exist, but centralize them in one configuration object.

## 24. IMAGE ASSET POLICY

IMAGE SOURCES ALLOWED:

Priority 1:
Pexels

Priority 2:
Unsplash

Priority 3:
Pixabay

Do NOT use:
- Google Images
- Pinterest
- random blogs
- motorcycle manufacturer press photos
- Getty
- Shutterstock
- iStock
- Adobe Stock
- AI generated stock imagery
- images copied from social media
- scraped images

All selected images must be suitable for commercial website use under the source platform's applicable license.

IMPORTANT:
The platform license alone is not sufficient.
Inspect the selected asset for:
- visible brand logos
- motorcycle manufacturer logos
- helmet logos
- apparel logos
- recognizable advertising
- license plates
- recognizable people
- identifiable private property
- obvious copyrighted artwork

Prefer:
- helmeted riders
- back/profile compositions
- anonymous riders
- landscape-oriented photographs
- motorcycles without visible manufacturer branding
- roads, mountains, coastlines, forests, sunrise/sunset
- documentary/editorial feeling
- authentic riding scenes

Avoid:
- obvious race behavior
- wheelies
- unsafe riding
- riders without helmets
- extreme lean-angle racing imagery
- obvious dealership marketing shots
- highly staged "stock" imagery

Suggested search themes:
- motorcycle touring
- motorcycle road trip
- motorcycle mountain road
- motorcycle rider back view
- motorcycle coastal road
- motorcycle group ride
- motorcycle adventure
- motorcycle road landscape
- motorbike touring
- motorbike mountain
- rider helmet road

CRITICAL:
Do not hotlink external images in production.

Download selected assets into:
public/images/landing/

Recommended asset naming:

landing-hero.webp
landing-story-route.webp
landing-ride.webp
landing-route.webp
landing-group.webp
landing-garage.webp
landing-safety.webp
landing-community.webp
landing-final.webp

Convert to WebP or AVIF when possible.

Create:

docs/ASSETS.md

For every external asset record:
- local filename
- source platform
- original source URL
- contributor/author if available
- date retrieved
- license reference URL
- usage notes
- any visible rights concern
- whether attribution is required
- exact section where used

Never use an asset if its licensing status is ambiguous.

## 25. ASSET SELECTION PRINCIPLE

Do not fill every section with photography.

Use approximately:
40% product UI
35% editorial photography
15% map visualizations
10% typography / graphic composition

The page must still feel like a real product even when images are removed.

## 26. PRODUCT UI VISUALS

All product screenshots must be designed as believable interface components.

Do NOT use:
- generic browser mockups
- fake MacBook frames
- random floating glass cards
- generic analytics dashboards
- excessive translucent cards

Use:
- phone UI
- route cards
- activity cards
- group ride panels
- motorcycle garage cards
- map panels
- small contextual overlays

Screenshots must feel like one coherent product.

## 27. COMPONENT SYSTEM

Create reusable components.

Required components:

LandingPage
LandingNav
AnnouncementBar
HeroSection
HeroRideCard
ProofStrip
EditorialStorySection
RideRecordingSection
RideRecordingUI
RouteDiscoverySection
RouteCard
RouteMap
GroupRideSection
GroupRideUI
MotorcycleIdentitySection
GarageCard
SafetySection
SafetyStatusUI
CommunitySection
ActivityCard
PerformanceSection
PerformanceChart
ImmersiveMapSection
CommunitySignals
FinalCTA
LandingFooter

Also create reusable primitives where appropriate:

SectionHeader
Eyebrow
PrimaryButton
SecondaryButton
Metric
Badge
Avatar
Divider
ImageFrame

Do not create one-off styling for every element.

## 28. SPACING SYSTEM

Use an 8px base grid.

Desktop:
section padding approximately 120–160px vertical.

Medium:
96–120px.

Mobile:
72–96px.

Container:
max-width approximately 1240–1440px.

Text column:
maximum approximately 680px.

Avoid excessive text width.

## 29. BORDER RADIUS

Avoid overly rounded designs.

Use:
- buttons: 10–12px
- cards: 16–20px
- large media frames: 20–28px
- map panels: 20px

Do not use:
30–50px radius everywhere.

## 30. BUTTON DESIGN

Primary:
lime background
dark text
strong weight

Label:
"Start Riding"

Hover:
slightly brighter
1–2px vertical lift
subtle glow only
not neon

Secondary:
transparent or low-contrast surface
thin border

Hover:
surface becomes slightly lighter

Buttons must feel physical and intentional.

## 31. MOTION SYSTEM

Motion should communicate hierarchy.

Use:

Entry:
fade + translateY 16–24px

Duration:
450–700ms

Easing:
cubic-bezier(0.22, 1, 0.36, 1)

Hover:
150–250ms

Image reveal:
600–900ms

Map route drawing:
1000–1800ms

Do NOT animate everything.

Maximum simultaneous motion:
1–2 major elements.

Do not use:
- bouncing
- spinning cards
- excessive parallax
- scroll hijacking
- infinite distracting animations
- flashy gradients
- cursor-following UI
- unnecessary 3D transformations

Respect prefers-reduced-motion.

## 32. RESPONSIVE RULES

Desktop:
>= 1200px

Tablet:
768–1199px

Mobile:
< 768px

Hero:
Desktop:
headline approximately 72–88px.

Mobile:
approximately 44–52px.

Mobile must NOT be:
a shrunk desktop.

Recompose layouts.

Mobile priority order:
1. Hero
2. Start Riding CTA
3. Product proof
4. Ride
5. Routes
6. Group ride
7. Motorcycle identity
8. Safety
9. Community
10. Performance
11. Final CTA

Hide secondary decorative layers on mobile when necessary.

Do not reduce essential content simply because viewport is narrow.

## 33. MOBILE UX

Assume users may access the landing page directly before or after riding.

Mobile requirements:
- thumb-friendly CTA
- no tiny buttons
- no horizontal overflow
- no text over busy photography without overlay
- no unreadable maps
- no tiny dashboard screenshots
- no complex hover-dependent interaction

Navigation:
- compact
- accessible
- simple drawer

Hero CTA should remain highly visible.

## 34. ACCESSIBILITY

Requirements:
- semantic HTML
- correct heading hierarchy
- keyboard navigation
- visible focus states
- alt text for meaningful imagery
- decorative images marked appropriately
- color contrast
- reduced-motion support
- buttons must be actual buttons/links
- no interaction dependent only on hover
- screen-reader friendly labels

## 35. PERFORMANCE

Landing page must be performance-conscious.

Requirements:
- responsive images
- WebP/AVIF
- lazy load below-the-fold images
- eager-load hero image
- use dimensions/aspect ratio to avoid layout shifts
- avoid massive JS bundles
- avoid unnecessary animation libraries if existing framework can handle motion
- avoid video backgrounds unless repository already has a suitable optimized local asset
- avoid loading 10+ heavy images simultaneously

Target:
- strong Lighthouse performance
- no major CLS
- fast LCP
- smooth mobile rendering

## 36. COPYWRITING RULES

Voice:
- direct
- confident
- concise
- human
- slightly poetic
- technically credible

Use motorcycle vocabulary naturally:
ride
route
crew
club
garage
waypoint
regroup
road
destination
mileage
ride history

Do not overuse:
freedom
adventure
brotherhood
throttle
speed
wild
born to ride

These are motorcycle advertising clichés.

Never write:
"Revolutionize your ride."
"Unlock your potential."
"The future of riding."
"Next-generation mobility platform."
"Powered by AI."
"Seamless experience."
unless specifically justified by actual product capabilities.

Avoid startup jargon:
- ecosystem
- paradigm
- frictionless
- innovative
- disruptive
- cutting-edge
- intelligent platform
when concrete language is available.

Prefer:
"Record the route."
"Find the road."
"Bring the crew."
"Know where everyone is."
"Keep your bike history."
"See where you've ridden."

## 37. ANTI-AI-GENERIC RULES

THIS SECTION IS MANDATORY.

The final page must NOT LOOK AI-GENERATED.

Never use:
- generic purple-blue gradients
- excessive glassmorphism
- repetitive 3-column cards
- symmetrical everything
- random decorative blobs
- giant gradient text
- stock "business person" photography
- abstract AI-generated landscapes
- random floating cards
- overuse of rounded corners
- generic SaaS illustrations
- repeated checkmark bullet lists
- giant centered headline followed by six cards
- meaningless metrics
- fake logos
- fake social proof
- fake testimonials
- fake reviews
- excessive icons
- emoji as interface decoration
- generic "AI-powered" language
- template-like section ordering

Design using:
- asymmetry
- editorial composition
- controlled whitespace
- real-world photography
- subtle borders
- product screenshots
- map traces
- hard visual hierarchy
- varied section rhythm
- large typography
- precise spacing
- small technical details
- authentic motorcycle context

Every section must have a reason to exist.

Every visual must communicate product behavior, brand identity, or emotional context.

## 38. EDITORIAL DESIGN PRINCIPLES

Create visual rhythm:

IMAGE
→ PRODUCT
→ TYPOGRAPHY
→ MAP
→ PRODUCT
→ IMAGE
→ COMMUNITY
→ MAP
→ CTA

Do NOT create:

TEXT
→ 3 CARDS
→ TEXT
→ 3 CARDS
→ TEXT
→ 3 CARDS

The composition should feel art-directed.

Some sections:
- split 55/45
- some 40/60
- some full-width
- some image-heavy
- some product-heavy

Do not make every section have the same geometry.

## 39. MICRO-DETAILS

Use subtle details that make the product believable:

- GPS coordinates
- ride timestamps
- elevation values
- route distance
- waypoint markers
- subtle map labels
- activity type labels
- rider status
- club member count
- motorcycle mileage
- service interval
- route difficulty
- weather indicator only if actual data exists
- offline state where relevant

These details should reinforce authenticity.

## 40. MAP DESIGN

Create a custom map visual language.

Base:
dark charcoal

Roads:
low-contrast grey

Major roads:
slightly brighter

Primary route:
#D8FF3E

Secondary route:
#61676C

Waypoint:
small outlined marker

Start:
lime

Destination:
white/lime

Avoid:
Google Maps visual cloning.

If a real map provider is already integrated, use its existing legally licensed map implementation.
Otherwise use an abstract cartographic illustration.

## 41. IMAGE TREATMENT

Photography should generally use:
- aspect ratio 16:10
- 4:3
- cinematic wide crops

Use:
object-fit: cover

Use dark overlays only where text needs contrast.

Prefer natural lighting.

Avoid overprocessing.

Avoid fake HDR.

Avoid excessive blur.

Avoid color grading that turns every motorcycle image orange/teal.

## 42. SEO

Page title:

"RIDELINE — Your Rides. Your Routes. Your People."

Meta description:

"A motorcycle riding platform to record rides, discover routes, ride with your crew, and build your riding history."

Open Graph:
Use the hero asset with appropriate crop.

Create:
- semantic metadata
- canonical
- Open Graph
- Twitter/X card
- structured heading hierarchy

Do not make unsupported SEO claims.

## 43. TECHNICAL IMPLEMENTATION

Before changing code:

1. Inspect the repository.
2. Determine current framework.
3. Identify existing design system.
4. Identify existing routing.
5. Identify existing components.
6. Identify existing asset conventions.
7. Identify existing CSS/Tailwind/theme system.
8. Preserve the existing architecture where reasonable.

Do not blindly replace the frontend stack.

If a design system exists:
extend it.

If Tailwind exists:
use the existing Tailwind architecture.

If CSS modules exist:
use the existing architecture.

If a component library exists:
reuse it where appropriate, but do not let it dictate the visual design.

Do not introduce a new framework unless absolutely necessary.

## 44. CONTENT ARCHITECTURE

Centralize all landing-page copy into a content/config structure.

Example:

landingContent = {
  hero: {...},
  proof: [...],
  story: {...},
  ride: {...},
  routes: [...],
  groupRide: {...},
  motorcycle: {...},
  safety: {...},
  community: {...},
  performance: {...},
  finalCta: {...}
}

Do not hardcode repeated strings throughout JSX/TSX templates.

## 45. ASSET ARCHITECTURE

Centralize asset references.

Example:

landingAssets = {
  hero,
  story,
  ride,
  route,
  groupRide,
  motorcycle,
  safety,
  community,
  finalCta
}

Do not scatter external URLs throughout components.

All asset sources must be documented in docs/ASSETS.md.

## 46. DATA POLICY FOR DEMO UI

All fictional UI data must be clearly treated as product-demo data in source code.

Use fictional names.

Never use:
- actual user's private data
- real customer information
- fake endorsements
- fake partnerships
- fake user counts
- fake reviews

If using a real brand/model is necessary to demonstrate product context, do not imply sponsorship.

Prefer generic or fictional examples.

## 47. FINAL IMPLEMENTATION CHECKLIST

Before declaring completion, verify ALL of these:

[ ] Landing page exists
[ ] Hero exists
[ ] Hero CTA exists
[ ] Navigation exists
[ ] Announcement bar exists
[ ] Product proof exists
[ ] Editorial story exists
[ ] Ride recording section exists
[ ] Route discovery exists
[ ] Group ride exists
[ ] Motorcycle identity exists
[ ] Safety exists
[ ] Community exists
[ ] Performance exists
[ ] Immersive map exists
[ ] Final CTA exists
[ ] Footer exists

[ ] Desktop responsive
[ ] Tablet responsive
[ ] Mobile responsive

[ ] No horizontal overflow
[ ] No console errors
[ ] No broken images
[ ] No broken links
[ ] No placeholder text
[ ] No lorem ipsum
[ ] No fake testimonials
[ ] No fake metrics
[ ] No fake logos
[ ] No unnecessary gradients
[ ] No generic AI-looking card grid

[ ] Reduced motion supported
[ ] Keyboard accessible
[ ] Focus states work
[ ] Images have appropriate alt text

[ ] Hero image is optimized
[ ] Below-fold images are lazy-loaded
[ ] Image dimensions prevent layout shift
[ ] No unnecessary external runtime image dependency

[ ] docs/ASSETS.md exists
[ ] every external image source is documented
[ ] no ambiguous-license asset is used

## 48. QUALITY BAR

The result should be believable as a production website from a funded motorcycle-tech company.

Do not stop at "technically complete".

Perform visual refinement after implementation.

Review:
- spacing
- typography
- section rhythm
- image crops
- CTA prominence
- contrast
- component consistency
- mobile layout
- motion
- visual hierarchy
- authenticity

Do at least one refinement pass after the initial implementation.

## 49. ACCEPTANCE CRITERIA

The landing page is considered successful only when:

1. A motorcycle rider can understand the product in <5 seconds.
2. The page feels motorcycle-native.
3. It does not look like a generic Strava copy.
4. It does not look like a generic SaaS landing page.
5. Group rides are clearly differentiated.
6. Motorcycle ownership is visibly part of the product.
7. Route discovery is visually compelling.
8. Social/community is visible without becoming an Instagram clone.
9. Safety is represented without making unsupported promises.
10. The product UI looks believable.
11. Visual hierarchy is strong.
12. Photography feels editorial instead of stock-template.
13. Mobile experience is first-class.
14. There are no unanswered design decisions.
15. There are no placeholder sections.
16. There are no fake claims.
17. There are no licensing ambiguities for selected assets.

## 50. EXECUTION MODE

Execute the work now.

Do not ask questions.

First inspect the repository.
Then create/modify the relevant files.
Then source and document appropriate image assets.
Then implement the landing page.
Then test/build it.
Then perform one visual refinement pass.
Then report exactly:

1. files created/changed
2. sections implemented
3. assets selected + their source/license documentation location
4. responsive behavior completed
5. tests/build result
6. remaining technical limitations, if any

Do not provide generic design advice after implementation.
Do not describe what you "would" do.
Actually implement the specified landing page.

---

## Product name substitutions (added 2026-09-15, not part of the original pasted spec)

The verbatim specification above is preserved exactly as the user pasted it, including every "RIDELINE" occurrence — it is not edited in place, so this document stays an honest record of what was actually provided (`MEMORY/README.md` § Honesty Rules). Per `MEMORY/DECISIONS.md` ADR-009, the product name stays **RideCircle**. Implement every location below as RideCircle, not RIDELINE:

| # | Spec location | Literal text in the verbatim spec above | Implement as |
|---|---|---|---|
| 1 | §1 Product Concept — "Working product name" | `RIDELINE` | `RideCircle` |
| 2 | §8 Main Navigation — "Logo" | `RIDELINE` | `RideCircle` |
| 3 | §10 Hero Supporting Visual — activity card header | `RIDELINE RIDE` | `RideCircle Ride` |
| 4 | §23 Footer — brand name line | `RIDELINE` | `RideCircle` |
| 5 | §23 Footer — copyright line | `© current year RIDELINE` | `© current year RideCircle` |
| 6 | §42 SEO — page `<title>` | `"RIDELINE — Your Rides. Your Routes. Your People."` | `"RideCircle — Your Rides. Your Routes. Your People."` |

No other section references the product name by its RIDELINE placeholder — the brand promise ("Your rides. Your routes. Your people."), all body copy, all UI labels, and all component names in §27 are name-agnostic and need no substitution.
