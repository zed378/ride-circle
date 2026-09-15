# Coding Standards & Guidelines — iOS

Native iOS app for RideCircle. Swift + SwiftUI + MVVM, per `MEMORY/DECISIONS.md` ADR-006.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Naming Conventions](#2-naming-conventions)
3. [Project Structure](#3-project-structure)
4. [Architecture (MVVM)](#4-architecture-mvvm)
5. [Dependency Injection](#5-dependency-injection)
6. [Networking](#6-networking)
7. [Local Storage (SwiftData)](#7-local-storage-swiftdata)
8. [Location & Background Recording](#8-location--background-recording)
9. [SwiftUI Standards](#9-swiftui-standards)
10. [Concurrency (async/await)](#10-concurrency-asyncawait)
11. [Error Handling](#11-error-handling)
12. [Testing Standards](#12-testing-standards)
13. [Git & Commit Conventions](#13-git--commit-conventions)

---

## 1. Project Overview

### Technology Stack

| Component | Technology | Notes |
|---|---|---|
| Language | Swift 5.10+ | |
| UI | SwiftUI | No UIKit except where SwiftUI genuinely can't do something (rare for MVP's screens) |
| Architecture | MVVM + unidirectional data flow | View → ViewModel (`@Observable`) → Repository → Service |
| Async | Swift Concurrency (`async`/`await`, actors) | No Combine unless a specific API only exposes a `Publisher` |
| Networking | `URLSession` + `Codable` | No third-party networking library needed at MVP scale |
| Local storage | SwiftData | GPS point buffering, offline ride cache |
| Background work | `CLLocationManager` background updates + `BGTaskScheduler` (upload retry) | |
| Navigation | `NavigationStack` (SwiftUI native) | |
| Testing | Swift Testing (or XCTest if the toolchain version predates it), XCUITest | |
| Min iOS version | iOS 17 | Enables `@Observable` and SwiftData without compatibility shims |

### Project Structure

```
ios/
├── docs/
│   └── CODING_STANDARDS.md
├── RideCircle/
│   ├── RideCircleApp.swift               # @main App entry point
│   ├── Core/
│   │   ├── Networking/                   # APIClient, endpoint definitions, DTOs
│   │   ├── Persistence/                  # SwiftData models, container setup
│   │   ├── Location/                     # LocationSampler, RecordingSession — docs/13-GPS/
│   │   └── DI/                           # Simple dependency container
│   ├── Features/
│   │   ├── Auth/
│   │   │   ├── Views/                    # LoginView.swift, RegisterView.swift
│   │   │   ├── AuthViewModel.swift
│   │   │   └── AuthRepository.swift
│   │   ├── Record/
│   │   │   ├── Views/                    # RecordView.swift, RideSummaryView.swift
│   │   │   ├── RecordViewModel.swift
│   │   │   └── RideRepository.swift
│   │   ├── History/
│   │   ├── Feed/
│   │   └── Profile/
│   └── Navigation/
│       └── RideCircleNavigationStack.swift
├── RideCircleTests/                      # unit tests, mirrors Features/ structure
├── RideCircleUITests/
└── RideCircle.xcodeproj
```

**Feature-per-folder**, mirroring the Android structure and `docs/01-PRD/` module boundaries — a developer moving between platforms should find the same shape.

---

## 2. Naming Conventions

Follow the [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/); project-specific additions below.

| Element | Convention | Example |
|---|---|---|
| Types (struct/class/enum/protocol) | `UpperCamelCase` | `RideRepository`, `RecordViewModel` |
| Functions/properties/variables | `lowerCamelCase` | `startRecording()`, `currentRide` |
| Constants | `lowerCamelCase` (Swift convention — not `UPPER_SNAKE_CASE`) | `let gpsSampleIntervalMs = 3000`, grouped in an `enum GpsConstants { static let ... }` namespace |
| SwiftUI Views | `UpperCamelCase`, suffix `View` | `RideSummaryView`, `RecordButtonView` |
| ViewModels | suffix `ViewModel`, marked `@Observable` | `RecordViewModel` |
| Repositories | suffix `Repository` | `RideRepository` |
| SwiftData models | plain domain noun, no suffix | `Ride`, `GpsPoint` (avoid `Entity` suffix — SwiftData models are the domain model here, unlike Room on Android) |
| DTOs (network layer only) | suffix `DTO` | `StartRideRequestDTO`, `RideSummaryResponseDTO` |
| Protocols describing capability | adjective/`-able`/`-ing` | `Recordable`, `LocationSampling` |

**File names match their primary type** — `RecordViewModel.swift` contains `RecordViewModel`, not multiple unrelated types.

---

## 3. Project Structure

Single app target is fine for MVP — don't split into Swift Packages per feature until the app genuinely needs the build-time isolation. `Core/` vs. `Features/` separation (§ above) captures most of the benefit already.

---

## 4. Architecture (MVVM)

```
SwiftUI View
   │  observes @Observable ViewModel, calls its methods on user action
   ▼
ViewModel (@Observable, @MainActor)
   │  holds UI state, calls Repository, maps domain results to UI state
   ▼
Repository
   │  decides local (SwiftData) vs. remote (APIClient) source, exposes domain models
   ▼
Service (APIClient / SwiftData ModelContext)
```

**Rules:**
- Views never call a Repository directly — only through a ViewModel.
- ViewModels are `@MainActor` (SwiftUI state must mutate on the main actor) but contain no `UIKit`/`SwiftUI` view code — keeps them testable in isolation.
- Repositories return domain models, not DTOs or SwiftData model types directly, where the two diverge — mapping happens at the repository boundary, matching the Android convention.

```swift
// Features/Record/RecordViewModel.swift
@Observable
@MainActor
final class RecordViewModel {
    private let rideRepository: RideRepository
    private let locationSampler: LocationSampling

    private(set) var uiState: RecordUiState = .idle

    init(rideRepository: RideRepository, locationSampler: LocationSampling) {
        self.rideRepository = rideRepository
        self.locationSampler = locationSampler
    }

    func startRecording() async {
        do {
            let ride = try await rideRepository.startRide()
            locationSampler.start(rideId: ride.id)
            uiState = .recording(rideId: ride.id)
        } catch {
            uiState = .error(error.localizedDescription)
        }
    }
}
```

---

## 5. Dependency Injection

No DI framework needed at this scale — plain initializer injection, assembled once at the app root:

```swift
// RideCircleApp.swift
@main
struct RideCircleApp: App {
    let apiClient = APIClient()
    let rideRepository: RideRepository

    init() {
        rideRepository = RideRepositoryImpl(apiClient: apiClient, modelContext: /* ... */)
    }

    var body: some Scene {
        WindowGroup {
            RideCircleNavigationStack()
                .environment(rideRepository)
        }
    }
}
```

Repositories are protocols (`RideRepository`) with a concrete implementation (`RideRepositoryImpl`) so tests can substitute a fake — same pattern as the Android `interface` + `Impl` convention.

---

## 6. Networking

- One `APIClient` wrapping `URLSession`, with typed endpoint definitions (an `enum Endpoint` or a small struct-per-request pattern) — no ad hoc `URLRequest` construction scattered through repositories.
- DTOs are `Codable` structs matching the backend's JSON field names via `CodingKeys` (backend uses `camelCase` JSON, matching Swift's default — minimal mapping needed).
- Auth token attached via a request-signing step in `APIClient`, refreshed transparently on `401` — feature code never manually attaches tokens.
- Map backend's `{success, status, message, data}` envelope (see `backend/docs/CODING_STANDARDS.md` §4) to a Swift `Result<T, APIError>` at the network boundary.

---

## 7. Local Storage (SwiftData)

- A `GpsPoint` SwiftData model buffers points locally during recording, per `docs/16-RIDE/02-RIDE-RECORDING.md` § Resilience — persisted in batches every ~10s, not per-point.
- A `Ride` SwiftData model mirrors in-flight and recently-completed rides for offline history access.
- Schema migrations use SwiftData's `VersionedSchema`/`SchemaMigrationPlan` explicitly — never ship a change that silently drops unsynced local data.

---

## 8. Location & Background Recording

The highest-stakes area of the iOS app — get it wrong and a rider loses a multi-hour ride.

- **Background modes**: `Location updates` capability enabled in `Info.plist`; `CLLocationManager` configured for `allowsBackgroundLocationUpdates = true` only while a ride is actively `recording`, turned back off on `stop`/`discard` (don't hold the background capability longer than needed).
- **Location requests**: `desiredAccuracy = kCLLocationAccuracyBest`, distance filter and sampling behavior matching `docs/13-GPS/01-LOCATION-SAMPLING.md` exactly (3s / 10m, ≤20m accuracy threshold) — implemented via a timer + distance check since `CLLocationManager` doesn't natively support "whichever comes first" sampling.
- **Points are flushed to SwiftData, not held only in memory** — app termination (iOS may kill backgrounded apps) must not lose more than the last unflushed batch (`docs/16-RIDE/02-RIDE-RECORDING.md` T1-02, T1-14).
- Request `Always` location authorization only when the recording flow actually needs it, with the in-app consent screen from `docs/45-COMPLIANCE/03-LOCATION-DATA.md` shown **before** the OS permission dialog. Requesting `Always` upfront at first launch (before the rider has tried recording) is exactly the anti-pattern App Review flags — request it contextually, at the moment of first "Start ride."

---

## 9. SwiftUI Standards

- **Views own no business logic** — formatting is fine (`String(format: "%.1f km", distanceKm)`), calculation is not.
- **`@Observable` ViewModel injected via `@Environment` or explicit `init`**, not global singletons reached into from inside a `View` body.
- **Previews**: every non-trivial view gets a `#Preview` with representative fake data.
- **Theming**: a single `RideCircleTheme` (custom `EnvironmentValues` or a `Color`/`Font` namespace) — no hardcoded `Color(red:green:blue:)` scattered through feature views.

---

## 10. Concurrency (async/await)

- Repository and service functions are `async throws` — no completion-handler-based APIs in new code.
- `Task { }` launched from a View or ViewModel action is scoped to that ViewModel's lifetime where possible (store the `Task` handle, cancel in `deinit` if the view can disappear mid-request, e.g. during upload).
- Long-running background work (GPS sampling loop) is isolated in an `actor` or a dedicated class marked appropriately — avoid data races on the buffered-points array by construction, not by convention alone.

---

## 11. Error Handling

```swift
enum APIError: Error {
    case server(status: Int, message: String)
    case network(underlying: Error)
    case decoding(underlying: Error)
}
```

ViewModels catch `APIError` and map it to a UI-facing enum (`RecordUiState.error(message:)`) — views `switch` over that state exhaustively.

---

## 12. Testing Standards

| Layer | Tool | Covers |
|---|---|---|
| Unit | Swift Testing (`@Test`) / XCTest | ViewModels (with a fake Repository), pure logic (distance/speed if duplicated client-side for live display) |
| UI | XCUITest | Screen rendering, user interaction flows |
| Manual | — | Real-device GPS recording in the field — background-mode survival, multi-hour battery behavior; not realistically automatable for MVP |

Every edge case listed on a `TASKS/PHASE-1-MVP-TRACKING.md` task needs at least a manual verification note if it can't be unit-tested, per `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done.

---

## 13. Git & Commit Conventions

Follow `TASKS/00-TASK-CONVENTIONS.md` exactly:

- Branch: `feat/T1-03-recording-session`
- Commit subject: `T1-03: implement background location recording session`
- PR body: task ID, `docs/` sections implemented, test layers added/run, any deviation with its ADR link.
