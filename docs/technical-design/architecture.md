# Architecture

## Overview

TGPM Backend is a Python service built on **connexion 3.x** (ASGI, wrapping Flask) that
exposes a REST API defined by the TGPM OpenAPI specification. It fetches geopolitical
event data from the **Wikidata SPARQL endpoint** and returns it as paginated JSON.

## Layer diagram

```
HTTP client
     │
     ▼
connexion (ASGI middleware)
  ├── validates request against openapi.yaml
  ├── routes operationId → controller via VersionedResolver
     │
     ▼
Controller  (src/main/event_resolver/controllers/)
  ├── accepts validated, pythonic-cased parameters
  ├── delegates entirely to the service layer
  └── calls .to_dict() on the response body model before returning
     │
     ▼
Service  (src/main/event_resolver/service/)
  ├── computes pagination math (totalPages, hasNextPage)
  ├── calls storage functions (count + paginated fetch)
  ├── calls mapper for each SPARQL binding
  └── constructs response body model (EventEventListResponseBody, etc.)
     │
     ├──────────────────────────────────────────────┐
     ▼                                              ▼
Mapper                                         SPARQL storage
(src/main/event_resolver/mapper/)              (src/main/event_resolver/persistence/repository/)
  ├── converts SPARQL binding dict                ├── builds SPARQL query from filters
  │   to generated model instance                ├── calls Wikidata SPARQL endpoint
  └── uses static lookup tables                  └── returns raw binding dicts
       (wikidata_class_enum, region_country_map)
                                                      │
                                                      ▼
                                               Wikidata SPARQL endpoint
                                               https://query.wikidata.org/sparql
```

## Component responsibilities

| Component | Location | Responsibility |
|---|---|---|
| `VersionedResolver` | `event_resolver/resolver.py` | Routes connexion operationIds to controller functions by prefix |
| Controllers | `event_resolver/controllers/` | HTTP parameter intake; calls service; serialises response with `.to_dict()` |
| Services | `event_resolver/service/` | Orchestration, pagination math, model construction |
| Mappers | `event_resolver/mapper/` | Converts SPARQL binding dicts to generated model instances |
| SPARQL storage | `event_resolver/persistence/repository/` | Executes COUNT and paginated SELECT queries against Wikidata |
| Static models | `event_resolver/persistence/models/` | Q-code enums and region→country maps (no I/O) |
| Generated models | `@generated/openapi_models/models/` | OpenAPI schema classes — never edit by hand |
| `__main__.py` | `src/main/__main__.py` | App factory; registers resolver, health route, SPARQL error handler |

## Import constraints

```
Controller   → service/ only
Service      → persistence/, mapper/
Mapper       → persistence/models/, @generated/
SPARQL storage → persistence/models/
Static models  → (nothing)
Generated      → (nothing in event_resolver/)
```

Circular imports break test isolation. Never import across the boundary in the wrong
direction.

## Routing

connexion loads `src/main/@generated/openapi_models/openapi/openapi.yaml` at startup.
Each path has an `operationId` (e.g. `v2_events_get`). `VersionedResolver` matches the
operationId prefix against `_ROUTES` and imports the corresponding controller module:

| Prefix | Controller module |
|---|---|
| `v1_events_` | `event_resolver.controllers.events_controller` |
| `v2_events_` | `event_resolver.controllers.events_v2_controller` |
| `v2_metadata_` | `event_resolver.controllers.events_v2_metadata_controller` |

The `x-openapi-router-controller` extension is stripped from `openapi.yaml` during
post-processing in `scripts/openapi.sh` so connexion never tries to auto-import
non-existent `openapi_models.controllers.*` modules.

## Data flow — paginated Wikidata endpoint

```
GET /v2/events?page=2&pageSize=20&types=WARFARE_AND_ARMED_CONFLICTS

connexion validates params → v2_events_get(page=2, page_size=20, types=["WARFARE_AND_ARMED_CONFLICTS"])
  → events_v2_service.get_events_v2(...)
      → count_events_v2(filters)         # SPARQL COUNT query → int
      → get_event_dao_list_v2(filters, page=2, page_size=20)  # SPARQL SELECT → list[dict]
      → map_binding(binding) * N         # each dict → EventEvent instance
      → Pagination(page=2, page_size=20, total_items=..., ...)
      → EventEventListResponseBody(data=[...], pagination=...)
  → result.to_dict()                     # applies attribute_map for camelCase JSON keys
HTTP 200  {"data": [...], "pagination": {"page": 2, "pageSize": 20, ...}}
```

## Error handling

| Exception | HTTP response |
|---|---|
| `EndPointInternalError` | 502 — upstream data source unavailable |
| `EndPointNotFound` | 502 — upstream data source unavailable |
| Unhandled exception | 500 (connexion default) |

The SPARQL error handler is registered in `src/main/__main__.py`.
