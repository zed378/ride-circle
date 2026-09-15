# Coding Standards & Guidelines — Backend

NestJS + TypeScript + Prisma backend for RideCircle. Framework rationale: `MEMORY/DECISIONS.md` ADR-010 (supersedes ADR-007). Storage rationale: ADR-011.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Naming Conventions](#2-naming-conventions)
3. [File Structure & Templates](#3-file-structure--templates)
4. [Response Format](#4-response-format)
5. [Error Handling](#5-error-handling)
6. [Validation](#6-validation-zod)
7. [Database & Prisma Standards](#7-database--prisma-standards)
8. [Auth & Guards](#8-auth--guards)
9. [Storage (Driver-Agnostic)](#9-storage-driver-agnostic)
10. [GPS / Ride Domain Standards](#10-gps--ride-domain-standards)
11. [Background Jobs (BullMQ)](#11-background-jobs-bullmq)
12. [Testing Standards](#12-testing-standards)
13. [Environment Variables](#13-environment-variables)
14. [Git & Commit Conventions](#14-git--commit-conventions)

---

## 1. Project Overview

### Technology Stack

| Component          | Technology                                                            | Notes                                                                                   |
| ------------------ | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Runtime            | Node.js 24 LTS                                                        |                                                                                         |
| Language           | TypeScript (strict mode)                                              | `"strict": true`, plus `experimentalDecorators` + `emitDecoratorMetadata` (NestJS DI)   |
| Framework          | NestJS (latest stable major, pinned at `T0-04`)                       | HTTP adapter: `@nestjs/platform-express` (the default) — Fastify not used               |
| Config             | `@nestjs/config`                                                      | Validated with a Zod schema at boot (§13)                                               |
| ORM                | Prisma                                                                | Wrapped in a `PrismaService` provider                                                   |
| Database           | PostgreSQL 17+                                                        | PostGIS extension enabled (ADR-010)                                                     |
| Cache / rate limit | Redis (`ioredis`), `@nestjs/throttler`                                | Throttler storage backed by Redis                                                       |
| Background jobs    | BullMQ via `@nestjs/bullmq`                                           | Redis-backed queues                                                                     |
| Validation         | Zod + a custom `ZodValidationPipe`                                    | Schema = runtime validator + static type, single source. **Not** class-validator        |
| Storage            | `StorageDriver` interface, `local` driver by default                  | Driver-agnostic; `s3` (S3-compatible) driver is a drop-in when needed (§9, ADR-011)     |
| Auth               | Custom JWT (`@nestjs/jwt`), `argon2` for password hashing             | Global guard, secure-by-default (§8). No Passport                                       |
| Testing            | Vitest + `unplugin-swc`, `@nestjs/testing`, Supertest                 | SWC is required: Vitest's default esbuild transform doesn't emit decorator metadata    |

Per `docs/07-DOMAIN/00-DOMAIN-MODEL.md` and `docs/47-ROADMAP/01-MVP-SCOPE.md`: only implement modules for `Status: MVP` documents. Do not scaffold code for Post-MVP entities (`Motorcycle`, `Club`, `Event`, etc.).

### Project Structure

```
backend/
├── docs/
│   └── CODING_STANDARDS.md            # This file
├── prisma/
│   ├── schema.prisma                  # Single source of truth for the DB schema
│   └── migrations/                    # Prisma-generated migration history
├── src/
│   ├── main.ts                        # Bootstrap: global filter/interceptor, shutdown hooks, listen
│   ├── app.module.ts                  # Root module — imports infra + feature modules
│   ├── config/
│   │   └── env.schema.ts              # Zod schema for env vars, used by ConfigModule.forRoot({ validate })
│   ├── common/                        # Cross-cutting, framework-level pieces — no domain logic
│   │   ├── constants/
│   │   │   ├── gps.constants.ts       # GPS_MAX_SPEED_KMH, ACCURACY_THRESHOLD_M, etc.
│   │   │   ├── ride.constants.ts      # SHORT_RIDE_DISTANCE_M, AUTO_PAUSE_THRESHOLD_MIN
│   │   │   └── pagination.constants.ts
│   │   ├── decorators/
│   │   │   ├── public.decorator.ts          # @Public() — opt out of rider auth
│   │   │   ├── admin-auth.decorator.ts      # @AdminAuth() — require admin token instead
│   │   │   ├── current-rider.decorator.ts   # @CurrentRider() param decorator
│   │   │   └── response-message.decorator.ts
│   │   ├── filters/
│   │   │   └── all-exceptions.filter.ts     # Error envelope (§5)
│   │   ├── guards/
│   │   │   └── auth.guard.ts                # Global: rider JWT by default, admin JWT on @AdminAuth()
│   │   ├── interceptors/
│   │   │   └── response-envelope.interceptor.ts  # Success envelope (§4)
│   │   ├── pipes/
│   │   │   └── zod-validation.pipe.ts
│   │   ├── pagination/
│   │   │   └── paginated.ts                 # Paginated<T> result type
│   │   └── utils/
│   │       ├── polyline.util.ts             # Google Polyline Algorithm encode/decode
│   │       └── haversine.util.ts
│   ├── infra/                         # Adapters to external systems, each a Nest module
│   │   ├── prisma/
│   │   │   ├── prisma.module.ts             # @Global
│   │   │   └── prisma.service.ts
│   │   ├── redis/
│   │   │   └── redis.module.ts              # Provides REDIS_CLIENT token
│   │   ├── queue/
│   │   │   └── queue.module.ts              # BullModule.forRootAsync + queue name constants
│   │   └── storage/                   # §9
│   │       ├── storage.module.ts            # Picks the driver from STORAGE_DRIVER
│   │       ├── storage-driver.interface.ts  # StorageDriver + STORAGE_DRIVER injection token
│   │       ├── storage-keys.ts              # The only place object keys are built
│   │       ├── public-files.controller.ts   # Serves public/* keys — local driver only
│   │       └── drivers/
│   │           ├── local.driver.ts          # Default: VM disk
│   │           └── s3.driver.ts             # Added when a deployment needs it (ADR-011)
│   └── modules/                       # One folder per domain module — matches docs/07-DOMAIN/
│       ├── health/
│       │   ├── health.module.ts
│       │   └── health.controller.ts
│       ├── auth/
│       │   ├── auth.module.ts
│       │   ├── auth.controller.ts
│       │   ├── auth.service.ts
│       │   ├── auth.schema.ts               # Zod schemas + inferred types
│       │   └── token.service.ts             # Issue/verify access + refresh tokens
│       ├── rider/
│       │   ├── rider.module.ts
│       │   ├── rider.controller.ts
│       │   ├── rider.service.ts
│       │   └── rider.schema.ts
│       ├── ride/
│       │   ├── ride.module.ts
│       │   ├── ride.controller.ts
│       │   ├── ride.service.ts
│       │   ├── ride.schema.ts
│       │   ├── ride.repository.ts           # Prisma queries isolated from business logic
│       │   ├── gps.service.ts               # distance/speed calculation, filtering — docs/13-GPS/
│       │   ├── raw-points.store.ts          # Reads/writes raw GPS points through StorageDriver
│       │   └── jobs/
│       │       ├── polyline.processor.ts
│       │       └── raw-points-purge.processor.ts
│       ├── social/
│       │   ├── social.module.ts
│       │   ├── social.controller.ts
│       │   ├── social.service.ts
│       │   ├── social.schema.ts
│       │   └── share-card.service.ts
│       └── admin/                     # Phase 3 (T3-04+) — don't create before those tasks start
│           ├── admin.module.ts
│           └── ...
├── test/
│   ├── unit/
│   ├── integration/
│   ├── e2e/                           # Supertest against a booted Nest app
│   └── fixtures/
├── storage/                           # Local driver root in dev — gitignored
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── nest-cli.json
├── vitest.config.ts
├── package.json
└── tsconfig.json
```

**Module-per-feature, not layer-per-folder.** Each domain module (`auth/`, `rider/`, `ride/`, `social/`) is one Nest module containing its controller, service, schema, and repository — matching `docs/07-DOMAIN/`'s module boundaries and making it obvious which files a given `docs/01-PRD/` document maps to.

**Dependency direction**: `modules/*` → `infra/*` and `common/*`. `infra/*` never imports from `modules/*`. A domain module that needs another module's logic imports that module and injects its **exported** service — never reaches into its repository or Prisma queries directly.

---

## 2. Naming Conventions

### File Names

`kebab-case`, suffixed by role — the Nest CLI convention:

- **Module**: `<name>.module.ts` (`ride.module.ts`)
- **Controller**: `<name>.controller.ts`
- **Service / provider**: `<name>.service.ts`
- **Schema (Zod)**: `<name>.schema.ts`
- **Repository** (only when a service's queries are complex enough to warrant separation): `<name>.repository.ts`
- **BullMQ processor**: `<job-name>.processor.ts`
- **Guard / interceptor / filter / pipe / decorator**: `<name>.guard.ts`, `.interceptor.ts`, `.filter.ts`, `.pipe.ts`, `.decorator.ts`
- **Utility**: `<name>.util.ts` — pure functions only, no DI
- **Constants**: `<domain>.constants.ts`

### Classes and Functions

- **Classes**: `PascalCase` + role suffix — `RideService`, `RideController`, `RiderJwtGuard`, `LocalStorageDriver`, `PolylineProcessor`.
- **Methods**: `camelCase`, verb-first — `startRide`, `stopRide`, `computeDistance`, `publishRide`, `followRider`.
- **Boolean-returning**: prefixed `is`/`has`/`can` — `isLowConfidencePoint`, `hasActiveSession`.
- **Repository methods**: prefixed by the CRUD verb they wrap — `findRideById`, `updateRideStatus`, `insertRidePauseEvent`.

### Variables and Types

- **Constants**: `UPPER_SNAKE_CASE` — `GPS_ACCURACY_THRESHOLD_M`, `MAX_SPEED_CAP_KMH` (see `docs/13-GPS/06-SPEED-CALCULATION.md` — the 220 km/h cap must be a named constant, never a literal in code).
- **Injection tokens**: `UPPER_SNAKE_CASE` symbols — `STORAGE_DRIVER`, `REDIS_CLIENT`.
- **Variables**: `camelCase`.
- **Types/Interfaces**: `PascalCase` — `RideSummary`, `GpsPoint`, `StorageDriver`. No `I` prefix.
- **Zod schemas**: `camelCase` ending in `Schema` — `startRideSchema`. Inferred type uses the matching `PascalCase` name: `type StartRideInput = z.infer<typeof startRideSchema>`.

### Prisma Model Names

- **Models**: `PascalCase`, singular — `Rider`, `Ride`, `RidePauseEvent`, `Track`, `Post`, `Follow`, `Kudos`, `Comment` (matches `docs/07-DOMAIN/` exactly — do not rename).
- **Table names** (via `@@map`): `snake_case`, plural — `riders`, `rides`, `ride_pause_events`.

---

## 3. File Structure & Templates

### Module Template

```typescript
// ride/ride.module.ts
import { Module } from "@nestjs/common";
import { BullModule } from "@nestjs/bullmq";
import { QUEUE_POLYLINE } from "../../infra/queue/queue.module";
import { RideController } from "./ride.controller";
import { RideService } from "./ride.service";
import { RideRepository } from "./ride.repository";
import { GpsService } from "./gps.service";
import { RawPointsStore } from "./raw-points.store";
import { PolylineProcessor } from "./jobs/polyline.processor";

@Module({
  imports: [BullModule.registerQueue({ name: QUEUE_POLYLINE })],
  controllers: [RideController],
  providers: [RideService, RideRepository, GpsService, RawPointsStore, PolylineProcessor],
  exports: [RideService], // only what other modules legitimately need
})
export class RideModule {}
```

`PrismaModule` and `StorageModule` are `@Global()`, so feature modules inject `PrismaService` / `STORAGE_DRIVER` without importing them.

### Service Template

```typescript
// ride/ride.service.ts
import { ConflictException, Injectable } from "@nestjs/common";
import { PrismaService } from "../../infra/prisma/prisma.service";
import type { StartRideInput } from "./ride.schema";

@Injectable()
export class RideService {
  constructor(private readonly prisma: PrismaService) {}

  async startRide(riderId: string, input: StartRideInput) {
    return this.prisma.ride.create({
      data: { riderId, status: "recording", startedAt: input.startedAt },
    });
  }

  async stopRide(rideId: string) {
    return this.prisma.$transaction(async (tx) => {
      const ride = await tx.ride.findUniqueOrThrow({ where: { id: rideId } });

      if (ride.status !== "recording" && ride.status !== "paused") {
        throw new ConflictException(`Cannot stop a ride with status "${ride.status}"`);
      }

      // ...compute summary via GpsService, update ride, increment rider stats

      return tx.ride.update({
        where: { id: rideId },
        data: { status: "completed", finishedAt: new Date() /* ...summary fields */ },
      });
    });
  }
}
```

- Services contain business logic and orchestrate Prisma calls. They **never** touch `Request`/`Response` objects — that keeps them unit-testable via `@nestjs/testing` without an HTTP layer.
- Multi-step writes that must be atomic (e.g. `stopRide`'s summary computation + rider stat increment, per `docs/16-RIDE/00-RIDE-LIFECYCLE.md`) use `prisma.$transaction`.
- Throw Nest's built-in `HttpException` subclasses (`NotFoundException`, `ConflictException`, `ForbiddenException`) — the global filter turns them into the envelope (§5).

### Controller Template

```typescript
// ride/ride.controller.ts
import { Body, Controller, Post } from "@nestjs/common";
import { CurrentRider, type AuthRider } from "../../common/decorators/current-rider.decorator";
import { ResponseMessage } from "../../common/decorators/response-message.decorator";
import { ZodValidationPipe } from "../../common/pipes/zod-validation.pipe";
import { startRideSchema, type StartRideInput } from "./ride.schema";
import { RideService } from "./ride.service";

@Controller("api/v1/rides")
export class RideController {
  constructor(private readonly rideService: RideService) {}

  /**
   * Start a new ride recording. See docs/01-PRD/04-RIDE-RECORDING.md.
   */
  @Post()
  @ResponseMessage("Ride started")
  startRide(
    @CurrentRider() rider: AuthRider,
    @Body(new ZodValidationPipe(startRideSchema)) body: StartRideInput,
  ) {
    return this.rideService.startRide(rider.id, body);
  }
}
```

- Controllers: validated input in → call **one** service method → return its result. No business logic, no Prisma, no manual envelope building.
- **Route paths are written in full** on `@Controller()` — `api/v1/...` for rider-facing routes, `admin/v1/...` for admin routes — instead of a global prefix, so a route is greppable by its public URL and the two auth surfaces are visually distinct.
- `POST` returns `201` by default in Nest; use `@HttpCode()` only when a different code is required (e.g. `@HttpCode(200)` on `POST api/v1/auth/login`).
- Reference the relevant `docs/` file in a JSDoc comment. Don't hand-maintain `@nestjs/swagger` annotations — OpenAPI generation is deferred (`docs/39-DEVELOPER/`, Post-MVP).

---

## 4. Response Format

Every endpoint returns the same envelope, matching `callibrator`'s shape for consistency across the team's APIs (the `web/`, `android/`, and `ios/` standards all depend on this section):

```typescript
// Success
{
  "success": true,
  "status": 200,
  "message": "Ride history fetched successfully",
  "data": { /* ... */ },
  "meta": { "total": 42, "page": 1, "limit": 20, "totalPages": 3 }  // only for paginated lists
}

// Error
{
  "success": false,
  "status": 404,
  "message": "Ride not found",
  "data": null
}
```

The success envelope is produced by one global interceptor; controllers just return data. Paginated service methods return a `Paginated<T>`, which the interceptor splits into `data` + `meta`:

```typescript
// common/pagination/paginated.ts
export class Paginated<T> {
  constructor(
    readonly items: T[],
    readonly meta: { total: number; page: number; limit: number; totalPages: number },
  ) {}
}
```

```typescript
// common/interceptors/response-envelope.interceptor.ts
@Injectable()
export class ResponseEnvelopeInterceptor implements NestInterceptor {
  constructor(private readonly reflector: Reflector) {}

  intercept(ctx: ExecutionContext, next: CallHandler) {
    const message =
      this.reflector.get<string>(RESPONSE_MESSAGE_KEY, ctx.getHandler()) ?? "Success";

    return next.handle().pipe(
      map((result) => {
        if (result instanceof StreamableFile) return result; // file downloads bypass the envelope
        const status = ctx.switchToHttp().getResponse<Response>().statusCode;
        if (result instanceof Paginated) {
          return { success: true, status, message, data: result.items, meta: result.meta };
        }
        return { success: true, status, message, data: result ?? null };
      }),
    );
  }
}
```

Registered once in `app.module.ts` as `{ provide: APP_INTERCEPTOR, useClass: ResponseEnvelopeInterceptor }`.

---

## 5. Error Handling

One global exception filter formats every error into the envelope — no ad hoc error responses in controllers.

```typescript
// common/filters/all-exceptions.filter.ts
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const res = host.switchToHttp().getResponse<Response>();
    const { status, message } = this.toHttp(exception);

    if (status >= 500) {
      // Log the error, never the request body — it may contain tokens or precise GPS traces
      this.logger.error(exception instanceof Error ? exception.stack : String(exception));
    }
    res.status(status).json({ success: false, status, message, data: null });
  }

  private toHttp(exception: unknown): { status: number; message: string } {
    if (exception instanceof HttpException) {
      const body = exception.getResponse();
      const message =
        typeof body === "string" ? body : [(body as { message?: unknown }).message].flat().join(", ");
      return { status: exception.getStatus(), message };
    }
    if (exception instanceof Prisma.PrismaClientKnownRequestError) {
      if (exception.code === "P2002") return { status: 409, message: "Resource already exists" };
      if (exception.code === "P2025") return { status: 404, message: "Resource not found" };
    }
    return { status: 500, message: "Internal server error" };
  }
}
```

Registered as `{ provide: APP_FILTER, useClass: AllExceptionsFilter }`.

- Use Nest's `HttpException` subclasses; don't invent a parallel `AppError` hierarchy.
- Prisma errors that represent a client mistake (unique violation, record not found) map to 4xx in the filter — services don't need to catch them just to rethrow.

**Never log**: JWTs, password hashes, raw GPS point arrays, storage object contents. Log the ride ID and rider ID, not the coordinates — per `docs/45-COMPLIANCE/03-LOCATION-DATA.md` and `AGENTS.md` hard rule 7. Nest's built-in `Logger` is the only logger; no `console.log` in committed code.

---

## 6. Validation (Zod)

One schema per endpoint payload, colocated in `<module>.schema.ts`, exporting both the schema and its inferred type:

```typescript
// ride/ride.schema.ts
import { z } from "zod";

export const uploadGpsPointsSchema = z.object({
  points: z
    .array(
      z.object({
        lat: z.number().min(-90).max(90),
        lng: z.number().min(-180).max(180),
        altitude: z.number().optional(),
        accuracyM: z.number().nonnegative(),
        timestamp: z.string().datetime(),
      }),
    )
    .min(1),
});

export type UploadGpsPointsInput = z.infer<typeof uploadGpsPointsSchema>;
```

```typescript
// common/pipes/zod-validation.pipe.ts
export class ZodValidationPipe<T extends ZodType> implements PipeTransform {
  constructor(private readonly schema: T) {}

  transform(value: unknown): z.infer<T> {
    const result = this.schema.safeParse(value);
    if (!result.success) {
      throw new BadRequestException(result.error.issues.map((i) => i.message));
    }
    return result.data;
  }
}
```

Apply the pipe per parameter: `@Body(new ZodValidationPipe(schema))`, `@Query(new ZodValidationPipe(listRidesQuerySchema))`. Services receive already-parsed, typed input and never re-validate it.

**Why not class-validator**: it would mean two validation systems (DTO classes for HTTP, Zod for env/config and job payloads) with two sets of error formats. Zod covers all three with one schema that is also the static type.

---

## 7. Database & Prisma Standards

- **Schema is the source of truth**: `prisma/schema.prisma` must match `docs/07-DOMAIN/` exactly — same field names (camelCase in Prisma, mapped to `snake_case` columns via `@map`), same constraints.
- **No Post-MVP models.** Do not add `Motorcycle`, `Club`, `Event`, etc. to `schema.prisma` ahead of need — see `docs/07-DOMAIN/00-DOMAIN-MODEL.md` § Catatan desain and `AGENTS.md` hard rule 5.
- **Migrations are additive** by default — a migration must not break a previous backend version mid-rollout (expand/contract pattern for any breaking schema change).
- **Constraints belong in the schema**, not just application code — `@@unique([riderId, postId])` for kudos, a `CHECK` constraint (via a raw SQL migration, since Prisma doesn't generate arbitrary `CHECK`s) for self-follow prevention.
- **Storage references are keys, never URLs or filesystem paths** — `Track.rawPointsRef` holds a storage key like `private/rides/<rideId>/raw-points.v1.json.gz` (§9). Switching storage drivers must never require a data migration.

```typescript
// infra/prisma/prisma.service.ts
@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit {
  async onModuleInit() {
    await this.$connect();
  }
}
```

`main.ts` calls `app.enableShutdownHooks()` so Prisma, Redis, and BullMQ workers close cleanly on `SIGTERM`.

```prisma
model Ride {
  id            String       @id @default(uuid())
  riderId       String       @map("rider_id")
  rider         Rider        @relation(fields: [riderId], references: [id])
  status        RideStatus
  visibility    Visibility   @default(private)
  startedAt     DateTime     @map("started_at")
  finishedAt    DateTime?    @map("finished_at")
  distanceKm    Decimal?     @map("distance_km")
  durationSec   Int?         @map("duration_sec")
  ridingTimeSec Int?         @map("riding_time_sec")
  avgSpeedKmh   Decimal?     @map("avg_speed_kmh")
  maxSpeedKmh   Decimal?     @map("max_speed_kmh")
  deletedAt     DateTime?    @map("deleted_at")

  @@map("rides")
}
```

---

## 8. Auth & Guards

- **Access token**: short-lived JWT (15 min), signed with a server-side secret (rotated via env, never hardcoded). **Refresh token**: longer-lived, stored server-side in Redis so it can be revoked (logout-everywhere).
- **Secure by default**: one global `AuthGuard` (`APP_GUARD`) protects every route. A route is only reachable anonymously if it's explicitly marked `@Public()` — forgetting a decorator fails closed, not open.
- **Admin auth is a separate flow** (`AGENTS.md` hard rule 10, `docs/01-PRD/21-ADMIN-MODERATION.md`): routes marked `@AdminAuth()` are verified against a **different secret** (`ADMIN_JWT_ACCESS_SECRET`) and resolve an `AdminUser`, never a `Rider`. A rider token presented to an admin route is rejected, and vice versa. No role flag on the rider JWT.

```typescript
// common/guards/auth.guard.ts
@Injectable()
export class AuthGuard implements CanActivate {
  constructor(
    private readonly reflector: Reflector,
    private readonly tokens: TokenService,
  ) {}

  async canActivate(ctx: ExecutionContext): Promise<boolean> {
    const targets = [ctx.getHandler(), ctx.getClass()];
    if (this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, targets)) return true;

    const req = ctx.switchToHttp().getRequest<Request>();
    const token = extractBearer(req);
    if (!token) throw new UnauthorizedException("Missing access token");

    if (this.reflector.getAllAndOverride<boolean>(IS_ADMIN_KEY, targets)) {
      req.admin = await this.tokens.verifyAdminAccess(token); // throws 401 on invalid/expired
    } else {
      req.rider = await this.tokens.verifyRiderAccess(token);
    }
    return true;
  }
}
```

- `@CurrentRider()` reads `req.rider`; it is never used on an `@AdminAuth()` route.
- **Login-failure lockout** (5 failed attempts / 15 min / account, `docs/01-PRD/01-AUTHENTICATION.md`) is implemented in `AuthService` with a Redis counter keyed by account — it's per-account, which `@nestjs/throttler` (per-client request rate) doesn't model. `@nestjs/throttler` with Redis storage is applied additionally to `api/v1/auth/*` as a general per-IP limit.
- Password hashing: `argon2`. Never return `passwordHash` from a service — select the fields you need.

---

## 9. Storage (Driver-Agnostic)

Raw GPS points and generated images (share cards, static map thumbnails) are stored through a `StorageDriver` interface. **No code outside `infra/storage/drivers/` knows which backend is in use.** The driver is chosen at boot by `STORAGE_DRIVER`; the default is `local` — the VM's own disk. Rationale and trade-offs: ADR-011.

### The interface

```typescript
// infra/storage/storage-driver.interface.ts
import type { Readable } from "node:stream";

export const STORAGE_DRIVER = Symbol("STORAGE_DRIVER");

export interface PutOptions {
  contentType: string;
}

export interface StorageDriver {
  /** Write (or overwrite) an object. Must be atomic: readers never see a partial object. */
  put(key: string, body: Buffer | Readable, options: PutOptions): Promise<void>;
  /** Stream an object. Throws StorageObjectNotFoundError if missing. */
  get(key: string): Promise<Readable>;
  exists(key: string): Promise<boolean>;
  /** Idempotent — deleting a missing key is not an error (retries of purge jobs must succeed). */
  delete(key: string): Promise<void>;
  /** Public URL for a `public/` key. Throws for any other key — private objects never get a URL. */
  publicUrl(key: string): string;
}
```

Deliberately small. Anything a driver can't implement identically everywhere (presigned uploads, lifecycle rules, listing) is **not** in the interface until a task actually needs it — adding it then means implementing it for every existing driver in the same change.

### Keys

- Built **only** by `storage-keys.ts` — no string-concatenated keys elsewhere.
- **Visibility is encoded in the key prefix**: `private/…` or `public/…`. This is the single rule every driver enforces, so "is this file publicly reachable?" never depends on driver configuration.
- Keys are relative, `/`-separated, lowercase, no `..`, no leading `/`. Include a format version when the file format may evolve.

```typescript
// infra/storage/storage-keys.ts
export const storageKeys = {
  rideRawPoints: (rideId: string) => `private/rides/${rideId}/raw-points.v1.json.gz`,
  shareCard: (postId: string, variant: "1x1" | "9x16") => `public/share-cards/${postId}/${variant}.png`,
  rideMapThumbnail: (rideId: string) => `public/ride-maps/${rideId}.png`,
};
```

Raw GPS points are **always** `private/` — they must never be served over HTTP (`docs/45-COMPLIANCE/03-LOCATION-DATA.md`). Only backend services and jobs read them.

### Driver selection

```typescript
// infra/storage/storage.module.ts
@Global()
@Module({
  controllers: [PublicFilesController],
  providers: [
    {
      provide: STORAGE_DRIVER,
      inject: [ConfigService],
      useFactory: (config: ConfigService<Env, true>): StorageDriver => {
        switch (config.get("STORAGE_DRIVER", { infer: true })) {
          case "local":
            return new LocalStorageDriver(
              config.get("STORAGE_LOCAL_ROOT", { infer: true }),
              config.get("STORAGE_PUBLIC_BASE_URL", { infer: true }),
            );
          // case "s3": return new S3StorageDriver(...)  — added with the driver (ADR-011)
        }
      },
    },
  ],
  exports: [STORAGE_DRIVER],
})
export class StorageModule {}
```

Consumers inject the token, never a concrete class:

```typescript
@Injectable()
export class RawPointsStore {
  constructor(@Inject(STORAGE_DRIVER) private readonly storage: StorageDriver) {}

  async save(rideId: string, points: GpsPoint[]): Promise<string> {
    const key = storageKeys.rideRawPoints(rideId);
    await this.storage.put(key, gzipSync(JSON.stringify(points)), { contentType: "application/gzip" });
    return key; // persisted as Track.rawPointsRef
  }
}
```

### `local` driver rules (default)

- Root directory from `STORAGE_LOCAL_ROOT` (dev: `./storage`, gitignored; Docker/VM: a mounted volume, e.g. `/var/lib/ridecircle/storage`). Created on boot if missing; boot fails if not writable.
- **Path-traversal guard**: resolve `path.resolve(root, key)` and reject any result that doesn't start with `root + path.sep`. Validate the key format before touching the filesystem.
- **Atomic writes**: write to a temp file in the same directory, then `rename` into place.
- **Public files** are served by `PublicFilesController` (`@Public()`) at `GET /files/public/*` — so `publicUrl(key)` is `${STORAGE_PUBLIC_BASE_URL}/${key}` — which only ever reads under `<root>/public/`, sets `Content-Type` and a long `Cache-Control` (keys are immutable or versioned). With any other driver it responds `404` for every path, and `publicUrl()` points at the bucket/CDN instead.
- The directory must be included in VM backups/snapshots — it is primary data, not a cache.

### Adding a driver

1. Implement `StorageDriver` in `drivers/<name>.driver.ts`.
2. Add the case to `StorageModule` and its env vars to the Zod env schema (required only when that driver is selected).
3. Run the shared **storage contract test suite** (`test/integration/storage/storage-driver.contract.ts`) against it — every driver must pass the same suite (atomic overwrite, idempotent delete, not-found error, `publicUrl` rejects `private/` keys, key validation).
4. Migrating existing data = copying the tree with identical keys. No database change.

---

## 10. GPS / Ride Domain Standards

This section exists because GPS/metric code is where a subtle bug becomes a wrong number shown to a rider — extra rigor applies here specifically.

- **Pure functions only** for distance/speed/filtering logic (`haversine.util.ts`, `GpsService`'s filtering methods) — no I/O, no `Date.now()` inside the calculation itself (pass timestamps in), so they're trivially unit-testable with fixed fixtures. `GpsService` has no injected dependencies for exactly this reason.
- **Every threshold is a named constant** in `common/constants/gps.constants.ts`, never an inline literal:
  ```typescript
  export const GPS_ACCURACY_THRESHOLD_M = 20;
  export const GPS_JUMP_MAX_DISTANCE_M = 500;
  export const GPS_JUMP_MAX_SECONDS = 3;
  export const MAX_SPEED_CAP_KMH = 220;
  export const SHORT_RIDE_DISTANCE_M = 500;
  export const SHORT_RIDE_DURATION_MIN = 2;
  ```
- **Every constant traces to a `docs/13-GPS/` or `docs/16-RIDE/` document** — if a threshold changes, update the doc in the same commit, not just the code (Deviation Protocol, `TASKS/00-TASK-CONVENTIONS.md`).
- **Test with synthetic fixtures**, not just real device data: a fixture file with a deliberate GPS jump, a low-confidence run, a pause/resume sequence — these are exactly the edge cases enumerated on each `TASKS/PHASE-1-MVP-TRACKING.md` task.
- **Raw points go through `RawPointsStore`** (§9), never into Postgres rows and never directly to `fs`.

---

## 11. Background Jobs (BullMQ)

- One queue per job type: `polyline-processing`, `share-card-render`, `raw-points-purge`. Queue names are exported constants from `infra/queue/queue.module.ts`.
- Processors live in the owning domain module (`ride/jobs/polyline.processor.ts`) as `@Processor(QUEUE_NAME)` classes extending `WorkerHost`.
- Job payloads are minimal (IDs, not full objects) — the processor re-fetches current data from Postgres, avoiding stale-data bugs from a payload captured at enqueue time.
- Every processor is idempotent — re-running a job for the same `rideId` must not double-process (relevant directly to `T1-10`'s "double-completion" edge case). Storage deletes are idempotent by contract (§9), so a retried purge job is safe.
- **With the `local` storage driver, workers must see the same filesystem as the API** — run them in the same process/container, or mount the same volume. This is one of the constraints that makes switching to a cloud driver the prerequisite for scaling beyond one VM (ADR-011).

---

## 12. Testing Standards

| Layer       | Tool                                                                          | Covers                                                                                            |
| ----------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Unit        | Vitest                                                                        | Pure functions: `haversine.util.ts`, `GpsService` filtering, ride state machine transitions       |
| Unit (DI)   | Vitest + `@nestjs/testing`                                                    | Services with mocked providers (`Test.createTestingModule().overrideProvider(...)`)               |
| Integration | Vitest + a real Postgres (via `testcontainers` or a Docker Compose test DB)   | Prisma queries, transactions, constraint enforcement; storage contract suite per driver (§9)      |
| E2E (HTTP)  | Supertest against `app.getHttpServer()`                                       | Full request/response cycle through guard + pipe + controller + service + filter/interceptor      |

- `vitest.config.ts` uses `unplugin-swc` so decorator metadata is emitted — without it, Nest DI silently injects `undefined` in tests.
- E2E tests boot the real `AppModule` (with the test database and `STORAGE_DRIVER=local` pointed at a temp directory), so the global guard, envelope interceptor, and exception filter are exercised exactly as in production.
- Every edge case named in a `TASKS/PHASE-*.md` task card must have a corresponding test — this is not optional, per `TASKS/00-TASK-CONVENTIONS.md` § Global Definition of Done item 2.

---

## 13. Environment Variables

```bash
# .env.example
NODE_ENV=development
PORT=3000

DATABASE_URL=postgresql://user:pass@localhost:5432/ridecircle
REDIS_URL=redis://localhost:6379

JWT_ACCESS_SECRET=
JWT_REFRESH_SECRET=
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=30d
ADMIN_JWT_ACCESS_SECRET=          # separate from rider secrets (§8)

# Storage (§9) — local disk by default
STORAGE_DRIVER=local              # local | s3 (s3 only once that driver exists)
STORAGE_LOCAL_ROOT=./storage
STORAGE_PUBLIC_BASE_URL=http://localhost:3000/files

# Only required when STORAGE_DRIVER=s3
# S3_ENDPOINT=
# S3_REGION=
# S3_BUCKET=
# S3_ACCESS_KEY_ID=
# S3_SECRET_ACCESS_KEY=
# S3_PUBLIC_BASE_URL=

GOOGLE_OAUTH_CLIENT_ID=
```

Validated at boot by `ConfigModule.forRoot({ isGlobal: true, validate: (raw) => envSchema.parse(raw) })`, where `envSchema` (`config/env.schema.ts`) is a Zod schema — driver-specific variables are a discriminated union on `STORAGE_DRIVER`, so a missing S3 credential only fails boot when `s3` is actually selected. The app must fail fast with a clear message on a missing/invalid variable, not fail obscurely on first use. Read config through `ConfigService<Env, true>`, never `process.env` directly outside `env.schema.ts`.

---

## 14. Git & Commit Conventions

Follow `TASKS/00-TASK-CONVENTIONS.md` exactly:

- Branch: `feat/T1-06-gps-upload-endpoint`
- Commit subject: `T1-06: implement batch GPS point upload endpoint`
- PR body: task ID, `docs/` sections implemented, test layers added/run, any deviation with its ADR link.
