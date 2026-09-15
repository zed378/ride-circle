# Coding Standards & Guidelines — Android

Native Android app for RideCircle. Kotlin + Jetpack Compose + MVVM, per `MEMORY/DECISIONS.md` ADR-006.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Naming Conventions](#2-naming-conventions)
3. [Module & Package Structure](#3-module--package-structure)
4. [Architecture (MVVM)](#4-architecture-mvvm)
5. [Dependency Injection (Hilt)](#5-dependency-injection-hilt)
6. [Networking](#6-networking)
7. [Local Storage (Room)](#7-local-storage-room)
8. [Location & Background Recording](#8-location--background-recording)
9. [Compose UI Standards](#9-compose-ui-standards)
10. [Coroutines & Flow](#10-coroutines--flow)
11. [Error Handling](#11-error-handling)
12. [Testing Standards](#12-testing-standards)
13. [Git & Commit Conventions](#13-git--commit-conventions)

---

## 1. Project Overview

### Technology Stack

| Component | Technology | Notes |
|---|---|---|
| Language | Kotlin | No Java in new code |
| UI | Jetpack Compose | No XML layouts |
| Architecture | MVVM + unidirectional data flow | View → ViewModel → Repository → DataSource |
| DI | Hilt | |
| Async | Kotlin Coroutines + Flow | |
| Networking | Retrofit + OkHttp | |
| Local DB | Room | GPS point buffering, offline ride cache |
| Background work | `ForegroundService` (recording), `WorkManager` (upload retry) | |
| Navigation | Jetpack Navigation Compose | |
| Testing | JUnit5, Turbine (Flow testing), Compose UI Test, MockK | |
| Min SDK | API 26 (Android 8.0) | Covers foreground service types needed for location |

### Project Structure

```
android/
├── docs/
│   └── CODING_STANDARDS.md
├── app/
│   └── src/
│       ├── main/
│       │   ├── kotlin/com/ridecircle/
│       │   │   ├── RideCircleApp.kt          # @HiltAndroidApp Application class
│       │   │   ├── core/
│       │   │   │   ├── network/              # Retrofit setup, interceptors, DTOs
│       │   │   │   ├── database/             # Room database, DAOs, entities
│       │   │   │   ├── location/             # LocationSampler, RecordingService — docs/13-GPS/
│       │   │   │   └── di/                   # Hilt modules
│       │   │   ├── feature/
│       │   │   │   ├── auth/
│       │   │   │   │   ├── ui/               # LoginScreen.kt, RegisterScreen.kt
│       │   │   │   │   ├── AuthViewModel.kt
│       │   │   │   │   └── AuthRepository.kt
│       │   │   │   ├── record/
│       │   │   │   │   ├── ui/               # RecordScreen.kt, RideSummaryScreen.kt
│       │   │   │   │   ├── RecordViewModel.kt
│       │   │   │   │   └── RideRepository.kt
│       │   │   │   ├── history/
│       │   │   │   ├── feed/
│       │   │   │   └── profile/
│       │   │   └── navigation/
│       │   │       └── RideCircleNavHost.kt
│       │   └── res/
│       └── test/                             # unit tests, mirrors main/ package structure
│       └── androidTest/                      # instrumented + Compose UI tests
├── build.gradle.kts
└── settings.gradle.kts
```

**Feature-per-package.** Each `feature/<name>/` folder is close to self-contained (its own `ui/`, ViewModel, repository) — matches the module boundaries in `docs/01-PRD/`. `core/` holds cross-cutting infrastructure only (network client, database, DI, the location engine shared by `record`).

---

## 2. Naming Conventions

Follow the [Kotlin official style guide](https://kotlinlang.org/docs/coding-conventions.html); project-specific additions below.

| Element | Convention | Example |
|---|---|---|
| Classes/Objects/Interfaces | `PascalCase` | `RideRepository`, `RecordViewModel` |
| Functions/properties | `camelCase` | `startRecording()`, `currentRide` |
| Constants (top-level or companion `const val`) | `UPPER_SNAKE_CASE` | `GPS_SAMPLE_INTERVAL_MS`, `MAX_SPEED_CAP_KMH` |
| Composable functions | `PascalCase`, noun describing what it renders | `RideSummaryCard`, `RecordButton` |
| Compose state holders | suffix `State` | `RecordScreenState` |
| ViewModels | suffix `ViewModel` | `RecordViewModel` |
| Repositories | suffix `Repository` | `RideRepository` |
| Room entities | suffix `Entity` | `GpsPointEntity`, `RideEntity` |
| Room DAOs | suffix `Dao` | `GpsPointDao` |
| Retrofit DTOs | suffix `Dto` (request) / `Response` (response) | `StartRideRequestDto`, `RideSummaryResponse` |
| Sealed result/UI-state classes | suffix `UiState` or use a shared `Result<T>` wrapper (§11) | `RecordUiState.Recording` |

**Package names**: all lowercase, no underscores — `com.ridecircle.feature.record`, not `com.ridecircle.feature.recordScreen`.

---

## 3. Module & Package Structure

Single `app` module is fine for MVP scale — don't split into multiple Gradle modules (`:core`, `:feature:record`, etc.) until build times or team size actually demand it. Package-level separation (§ above) gets most of the benefit without the Gradle overhead.

---

## 4. Architecture (MVVM)

```
Composable (View)
   │  observes StateFlow, calls ViewModel functions on user action
   ▼
ViewModel
   │  holds UI state, calls Repository, maps domain results to UI state
   ▼
Repository
   │  decides local (Room) vs. remote (Retrofit) as data source, exposes domain models
   ▼
DataSource (Room DAO / Retrofit API interface)
```

**Rules:**
- Composables never call a Repository or DAO directly — only through a ViewModel.
- ViewModels never reference Android `Context`, `View`, or any Compose type — keeps them unit-testable without instrumentation.
- Repositories return domain models (plain Kotlin data classes), not Room entities or Retrofit DTOs directly — mapping happens at the repository boundary.

```kotlin
// feature/record/RecordViewModel.kt
@HiltViewModel
class RecordViewModel @Inject constructor(
    private val rideRepository: RideRepository,
    private val locationSampler: LocationSampler,
) : ViewModel() {

    private val _uiState = MutableStateFlow<RecordUiState>(RecordUiState.Idle)
    val uiState: StateFlow<RecordUiState> = _uiState.asStateFlow()

    fun startRecording() {
        viewModelScope.launch {
            val ride = rideRepository.startRide()
            locationSampler.start(ride.id)
            _uiState.value = RecordUiState.Recording(ride.id)
        }
    }
}
```

---

## 5. Dependency Injection (Hilt)

- `@HiltAndroidApp` on the `Application` class, `@AndroidEntryPoint` on Activities.
- One `@Module` per concern in `core/di/`: `NetworkModule`, `DatabaseModule`, `LocationModule`.
- Bind interfaces, not concrete classes, into the graph where a fake is needed for testing (`RideRepository` interface + `RideRepositoryImpl`).

---

## 6. Networking

- Retrofit interfaces live in `core/network/`, one per backend module matching `backend/src/modules/` (`AuthApi`, `RideApi`, `SocialApi`).
- All DTOs are `data class`es with `@Serializable` (kotlinx.serialization) or Moshi annotations — pick one project-wide, don't mix.
- Auth token attached via an OkHttp `Interceptor`, refreshed transparently on `401` via an `Authenticator` — UI code never manually attaches tokens.
- Map backend's `{success, status, message, data}` envelope (see `backend/docs/CODING_STANDARDS.md` §4) to a sealed `ApiResult<T>` at the network boundary — feature code never touches the raw envelope.

---

## 7. Local Storage (Room)

- `GpsPointEntity` buffers points locally during recording, per `docs/16-RIDE/02-RIDE-RECORDING.md` § Resilience — written in batches every ~10s, not per-point, to limit I/O.
- `RideEntity` mirrors in-flight and recently-completed rides for offline access to history.
- Migrations use Room's `Migration` objects explicitly — never `fallbackToDestructiveMigration()` in a release build, since that would silently discard a rider's unsynced ride data.

---

## 8. Location & Background Recording

This is the highest-stakes area of the Android app — get it wrong and a rider loses a multi-hour ride.

- **Foreground service** (`RecordingService`, `core/location/`) with `FOREGROUND_SERVICE_TYPE_LOCATION`, persistent notification showing live distance/duration, started the moment recording begins and stopped only on `stop`/`discard`.
- **Location requests**: `FusedLocationProviderClient`, priority `PRIORITY_HIGH_ACCURACY`, interval/params matching `docs/13-GPS/01-LOCATION-SAMPLING.md` exactly (3s / 10m, ≤20m accuracy threshold).
- **Points are flushed to Room, not held only in memory** — a process death mid-ride must not lose more than the last unflushed batch (`docs/16-RIDE/02-RIDE-RECORDING.md` T1-02, T1-14).
- Request `ACCESS_BACKGROUND_LOCATION` only when the recording flow actually needs it, with the in-app consent screen from `docs/45-COMPLIANCE/03-LOCATION-DATA.md` shown **before** the OS permission dialog.

---

## 9. Compose UI Standards

- **Stateless composables preferred**: a screen-level composable owns state (via `collectAsStateWithLifecycle()` from the ViewModel); child composables receive state and lambdas as parameters, no direct ViewModel access.
- **No business logic in composables** — formatting is fine (`"%.1f km".format(distanceKm)`), calculation is not (never compute `avgSpeed` inside a composable).
- **Previews**: every non-trivial composable gets a `@Preview` with representative fake data — catches obvious layout breaks without running the app.
- **Theming**: colors/typography/spacing come from a single `RideCircleTheme` (`MaterialTheme` customization) — no hardcoded `Color(0xFF...)` scattered in feature code.

---

## 10. Coroutines & Flow

- `viewModelScope` for ViewModel-launched work — never a manually-created `GlobalScope`.
- Repository functions that return a stream (e.g. "observe current ride state") return `Flow<T>`; one-shot operations (`startRide()`) are `suspend fun`.
- Use `StateFlow` for UI state (always has a current value), `SharedFlow` only for one-off events (snackbar messages, navigation triggers) that shouldn't replay on recomposition.

---

## 11. Error Handling

```kotlin
sealed interface ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>
    data class Error(val status: Int, val message: String) : ApiResult<Nothing>
    data object NetworkError : ApiResult<Nothing>
}
```

ViewModels map `ApiResult` to a UI-facing sealed state (`RecordUiState.Error(message)`, etc.) — screens render based on that sealed state exhaustively (`when` with no `else` branch), so a new state can't silently fall through unhandled.

---

## 12. Testing Standards

| Layer | Tool | Covers |
|---|---|---|
| Unit | JUnit5 + MockK | ViewModels (with fake Repository), pure logic (distance/speed if duplicated client-side for live display) |
| Flow | Turbine | `StateFlow`/`Flow` emissions from ViewModels and Repositories |
| Instrumented / Compose UI | Compose UI Test, Espresso where needed | Screen rendering, user interaction flows |
| Manual | — | Real-device GPS recording in the field — screen-lock survival, multi-hour battery behavior; not realistically automatable for MVP |

Every edge case listed on a `TASKS/PHASE-1-MVP-TRACKING.md` task (e.g. "app force-killed mid-ride → recoverable") needs at least a manual verification note if it can't be unit-tested, per `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done.

---

## 13. Git & Commit Conventions

Follow `TASKS/00-TASK-CONVENTIONS.md` exactly:

- Branch: `feat/T1-03-recording-service`
- Commit subject: `T1-03: implement foreground RecordingService`
- PR body: task ID, `docs/` sections implemented, test layers added/run, any deviation with its ADR link.
