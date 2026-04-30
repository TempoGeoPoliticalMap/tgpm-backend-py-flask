# Release Notes — 2.0.0

> **Branch:** `fix-cors`
> **Date:** 2026-04-30

---

## Summary

Release 2.0.0 makes the API usable from browser applications by adding **CORS support**, removes the legacy `/v1/events` endpoint, and advances the pinned OpenAPI spec to the latest version.

Browser-based frontends previously received `Response body is not available to scripts (Reason: CORS Missing Allow Origin)` on every request. All responses now carry the required `Access-Control-Allow-Origin` header, and preflight `OPTIONS` requests are answered before routing so no browser request is blocked. The allowed origins are configurable via an environment variable for production deployments.

All `/v2/*` endpoints are unchanged in behaviour and response shape.

---

## Breaking changes

### `GET /v1/events` removed

The `/v1/events` endpoint has been removed. Clients still using it must migrate to `GET /v2/events`, which provides a richer, structured response with filtering, pagination, geographic coordinates, Wikipedia links, and time-state classification. See the [1.0.0 release notes](../1.0.0/release-notes.md) for the full `/v2/events` reference.

---

## Release details

### CORS support

All API responses now include `Access-Control-Allow-Origin` so browser applications can read them. Browser preflight `OPTIONS` requests are intercepted before routing and answered with the appropriate `Access-Control-Allow-*` headers, preventing false 404 errors on preflight.

**Environment variable — `CORS_ALLOWED_ORIGINS`** (new, in `config.env`):

| Value | Behaviour |
|---|---|
| Unset or empty | Defaults to `*` — allows all origins. Acceptable for local development. |
| `https://app.example.com` | Restricts to a single origin. Recommended for production. |
| `https://app.example.com,http://localhost:3000` | Comma-separated list — allows multiple specific origins. |

Set this variable to the exact frontend origin before deploying to production. Leaving it unset (wildcard) in a public deployment means any website can call the API.

---

### OpenAPI spec update

The pinned spec SHA has been advanced from `775b078` to `c7d0fed`. The new spec renames several v2 model classes (e.g. `EventEvent` → `Event`). These are internal server-side names only — JSON response keys and API behaviour are unchanged.

---

## Infrastructure

- **CORS middleware:** `starlette.middleware.cors.CORSMiddleware` is now registered at the outermost middleware position (`BEFORE_ROUTING`), ensuring CORS headers are present on all responses including error responses and preflight replies.
- **`CORS_ALLOWED_ORIGINS`:** New environment variable documented in `config.env`. Supports comma-separated origin lists.

---

## Backward compatibility

`GET /v1/events` is **removed** in this release. This is an intentional breaking change — the version number advances to 2.0.0 to reflect it.

All `/v2/*` endpoints (`/v2/events`, `/v2/metadata/event-types`, `/v2/metadata/regions`, `/v2/metadata/country-codes`) are unchanged.

---

## Known constraints

- Default `CORS_ALLOWED_ORIGINS` is `*`. Set to exact origin(s) before production deployment.
- Default time window (when no `timeslot_start`/`timeslot_end` is provided) is **today only** (UTC midnight to 23:59:59).
- Default `pageSize` is **25** on all paginated endpoints; maximum is **100**.
- Country filter uses ISO 3166-1 alpha-3 codes; values not matching `[A-Z]{3}` are rejected with HTTP 400.
- Wikidata SPARQL latency may vary. Requests time out after 30 seconds.
