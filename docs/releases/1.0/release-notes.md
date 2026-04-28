# Release Notes — 1.0

> **Branch:** `support-v2-events`
> **Date:** 2026-04-28

---

## Summary

Release 1.0 introduces a new version of the events API (`/v2`) that replaces the raw Wikidata response of v1 with a clean, structured format designed for direct use in maps and timelines.

Clients can now query historical political events filtered by **type**, **region**, or **country**, with built-in **pagination** and pre-computed fields such as geographic coordinates, Wikipedia links, and whether each event is in the past, ongoing, or upcoming. Three supporting metadata endpoints provide the valid filter values for types, regions, and country codes.

The existing `GET /v1/events` endpoint is unchanged.

---

## Release details

### New endpoints

### `GET /v2/events`

Paginated, filterable list of historical political events backed by Wikidata SPARQL.

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | 1 | Page number (1-based) |
| `pageSize` | integer | 25 | Items per page (max 100) |
| `types` | enum[] | all | Filter by event type (see `/v2/metadata/event-types` for valid values) |
| `regions` | enum[] | all | Filter by world region (see `/v2/metadata/regions` for valid values) |
| `countries` | string[] | all | Filter by ISO 3166-1 alpha-3 country code (e.g. `GBR`, `FRA`) |
| `timeslot_start` | ISO 8601 | today 00:00:00Z | Events starting on or after this datetime |
| `timeslot_end` | ISO 8601 | today 23:59:59Z | Events starting on or before this datetime |

When `regions` and `countries` are both supplied, events matching either are returned (OR semantics).

**Response shape:**
```json
{
  "data": [
    {
      "wikidataId": "Q178810",
      "wikidataUrl": "https://www.wikidata.org/wiki/Q178810",
      "name": "Syrian Civil War",
      "type": "WARFARE_AND_ARMED_CONFLICTS",
      "startDateTime": "2011-03-15T00:00:00Z",
      "endDateTime": null,
      "timeStateRelativeToNow": "ONGOING",
      "description": "...",
      "imageUrl": "...",
      "wikipediaUrl": "https://en.wikipedia.org/wiki/Syrian_civil_war",
      "countries": [{ "wikidataId": "Q858", "name": "Syria" }],
      "locations": [{ "wikidataId": "Q858", "name": "Syria", "coordinate": "33.51,36.29" }],
      "regions": ["MIDDLE_EAST_AND_NORTH_AFRICA"]
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 25,
    "totalItems": 342,
    "totalPages": 4,
    "hasNextPage": true
  }
}
```

---

### `GET /v2/metadata/event-types`

Static list of the 10 supported event type filter values.

**Response:** `{ "data": [{ "code": "WARFARE_AND_ARMED_CONFLICTS", "name": "Warfare and Armed Conflicts", "description": "..." }, ...] }`

**Event types:**

| Code | Name |
|---|---|
| `GEOPOLITICAL_GROUP` | Geopolitical Group |
| `INTERNATIONAL_ORGANISATION` | International Organisation |
| `MILITARY_ALLIANCE` | Military Alliance |
| `MULTINATIONAL_MILITARY_COALITION` | Multinational Military Coalition |
| `POLITICAL_CONFERENCE` | Political Conference |
| `POLITICAL_CRISIS` | Political Crisis |
| `POLITICAL_MURDER` | Political Murder |
| `SOURCE_OF_INTERNATIONAL_LAW` | Source of International Law |
| `SUPRANATIONAL_UNION` | Supranational Union |
| `WARFARE_AND_ARMED_CONFLICTS` | Warfare and Armed Conflicts |

---

### `GET /v2/metadata/regions`

Static list of the 7 supported region filter values.

**Response:** `{ "data": [{ "code": "EUROPE_AND_CENTRAL_ASIA", "name": "Europe and Central Asia", "description": "..." }, ...] }`

**Regions:**

| Code | Name |
|---|---|
| `EAST_ASIA_AND_PACIFIC` | East Asia and Pacific |
| `EUROPE_AND_CENTRAL_ASIA` | Europe and Central Asia |
| `LATIN_AMERICA_AND_CARIBBEAN` | Latin America and Caribbean |
| `MIDDLE_EAST_AND_NORTH_AFRICA` | Middle East and North Africa |
| `NORTH_AMERICA` | North America |
| `SOUTH_ASIA` | South Asia |
| `SUB_SAHARAN_AFRICA` | Sub-Saharan Africa |

---

### `GET /v2/metadata/country-codes`

Paginated, searchable list of ISO 3166-1 alpha-3 country codes sourced from Wikidata.

**Query parameters:** `page`, `pageSize`, `q` (free-text search on code or name)

**Response:** `{ "data": [{ "code": "GBR", "name": "United Kingdom" }, ...], "pagination": { ... } }`

---

## Changes

### Infrastructure

- **Configurable port:** Server binds to the `PORT` environment variable (default `8080`) and listens on `0.0.0.0`.
- **Health check:** `GET /health` returns `{ "status": "ok" }` — used for container liveness probes.
- **Error handling:** Wikidata SPARQL errors are surfaced to clients as structured HTTP responses: `502` for endpoint errors, `504` for timeouts, `429` (with `Retry-After` header) for rate limiting.
- **Dockerfile:** Updated to Python 3.13; `@generated` directory added to `PYTHONPATH`.

### Code generation

- `scripts/openapi.sh` now fetches the OpenAPI spec from the remote repository at a pinned commit SHA, making code generation reproducible. The previous local-file approach is removed.

### Dependencies

All Python dependencies updated to their latest stable versions. Key bumps:

| Package | Previous | 1.0 |
|---|---|---|
| connexion | 3.1.0 | 3.3.0 |
| Flask | 3.0.3 | 3.1.3 |
| uvicorn | 0.32.0 | 0.46.0 |
| pydantic | 2.9.2 | 2.13.3 |
| starlette | 0.41.2 | 1.0.0 |
| jsonschema | 4.23.0 | 4.26.0 |
| httpx | 0.27.2 | 0.28.1 |
| PyYAML | 6.0.2 | 6.0.3 |
| rdflib | 7.1.1 | 7.6.0 |
| Werkzeug | 3.1.2 | 3.1.8 |
| Jinja2 | 3.1.4 | 3.1.6 |

Full audit in [`dependency-updates.md`](dependency-updates.md).

---

## Backward compatibility

`GET /v1/events` is unchanged and continues to work.

---

## Known constraints

- Default time window (when no `timeslot_start`/`timeslot_end` is provided) is **today only** (UTC midnight to 23:59:59).
- Default `pageSize` is **25** on all paginated endpoints; maximum is **100**.
- Country filter uses ISO 3166-1 alpha-3 codes; values not matching `[A-Z]{3}` are rejected with HTTP 400.
- Wikidata SPARQL latency may vary. Requests time out after 30 seconds.
