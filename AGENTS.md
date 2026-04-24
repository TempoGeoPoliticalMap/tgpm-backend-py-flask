# AGENTS.md

Read this file before making any change. It contains everything needed to understand the project, make a change safely, and add a new endpoint — without consulting any other file first.

---

## What this project does

TGPM Backend is a Python service built on **connexion 3.x** (ASGI, wrapping Flask) that serves historical geopolitical event data fetched from the **Wikidata SPARQL endpoint** (`https://query.wikidata.org/sparql`). It exposes a versioned REST API defined by the TGPM OpenAPI specification:

```
https://raw.githubusercontent.com/TempoGeoPoliticalMap/tgpm-openapi/<SPEC_SHA>/openapi.bundled.yaml
```

The pinned `SPEC_SHA` is recorded in `scripts/openapi.sh`. The server runs in a Docker container (`Dockerfile`). Auth (BearerAuth/JWT) is handled at the infrastructure level — never implement token validation in Python code.

---

## Quick-start commands

```bash
make setup             # install dependencies + activate pre-commit hooks (run once after clone)
make run               # start development server at http://localhost:8080
make test              # run all 60 tests (unit + integration)
make test-unit         # unit tests only (fast, no network)
make test-integration  # integration tests only
make lint              # ruff linter — reports issues, no file changes
make format            # ruff + black auto-format
make typecheck         # mypy static analysis
make openapi           # regenerate src/main/@generated/ from the remote OpenAPI spec
```

`PYTHONPATH` is set automatically by `make test*` targets. All tool configuration lives in `pyproject.toml`.

---

## Repository structure

```
tgpm-backend-py-flask/
├── AGENTS.md                  ← You are here. Read before making changes.
├── Makefile                   ← All common commands (setup, test, lint, format, run, openapi)
├── .pre-commit-config.yaml    ← gitleaks + ruff + black + mypy (runs on every git commit)
├── pyproject.toml             ← Dependency constraints + tool config (black, ruff, mypy, pytest)
├── requirements.txt           ← Auto-generated from Pipfile.lock by pre-commit hook — never edit by hand
├── Dockerfile                 ← Production container image
├── scripts/
│   └── openapi.sh             ← THE ONLY way to regenerate src/main/@generated/
├── docs/
│   ├── releases/              ← Per-release execution plans (read before starting work)
│   └── technical-design/      ← Architecture docs, SPARQL queries, Wikidata mappings
└── src/
    ├── main/
    │   ├── @generated/        ← AUTO-GENERATED — never edit by hand; re-run openapi.sh
    │   │   └── openapi_models/
    │   │       ├── models/    ← Generated model classes (EventEvent, Pagination, etc.)
    │   │       └── openapi/   ← openapi.yaml loaded by connexion at runtime
    │   ├── event_resolver/    ← ALL business logic lives here
    │   │   ├── controllers/   ← HTTP layer — one function per operationId in the spec
    │   │   ├── service/       ← Orchestration — pagination math, model construction
    │   │   ├── mapper/        ← Converts SPARQL binding dicts to model instances
    │   │   ├── persistence/
    │   │   │   ├── models/    ← Static lookup tables (Q-codes, region→country maps)
    │   │   │   └── repository/← SPARQL query functions (COUNT + SELECT)
    │   │   └── resolver.py    ← VersionedResolver: routes operationIds to controllers
    │   └── __main__.py        ← App entry point: resolver, health route, SPARQL error handler
    └── test/
        └── python/
            ├── unit/          ← Unit tests — no network, all deps mocked
            └── test_events/   ← Integration tests — full HTTP stack, storage mocked
```

---

## The generated / custom boundary

**`src/main/@generated/` is owned by the OpenAPI generator. Any hand-edit will be lost the next time `openapi.sh` runs.**

Custom code lives exclusively in `src/main/event_resolver/`. Generated model classes are imported by custom code — never copied or modified.

When the upstream spec changes:
1. Run `make openapi`
2. Inspect new model classes in `src/main/@generated/openapi_models/models/`
3. Update imports and mapper code in `src/main/event_resolver/` as needed
4. Run `make test`

`openapi.sh` applies two post-processing fixes after generation:
- Strips `x-openapi-router-controller` and `x-bearerInfoFunc` from `openapi.yaml`
- Patches `base_model.py` so `to_dict()` uses `attribute_map` values as JSON keys (for camelCase serialisation)

---

## Layer rules

```
Layer               Location                        May import from
─────────────────────────────────────────────────────────────────────────────────────────
Controller          controllers/                    service/ only
Service             service/                        persistence/, mapper/
Mapper              mapper/                         persistence/models/, @generated/
SPARQL storage      persistence/repository/         persistence/models/
Static models       persistence/models/             (nothing)
Generated           @generated/                     (nothing in event_resolver/)
```

Violations create circular imports and break test isolation.

---

## Routing

connexion loads `src/main/@generated/openapi_models/openapi/openapi.yaml` at startup. Each path has an `operationId`. `VersionedResolver` (`event_resolver/resolver.py`) routes by prefix:

| operationId prefix | Controller module |
|---|---|
| `v1_events_` | `event_resolver.controllers.events_controller` |
| `v2_events_` | `event_resolver.controllers.events_v2_controller` |
| `v2_metadata_` | `event_resolver.controllers.events_v2_metadata_controller` |

connexion's `pythonic_params=True` converts camelCase query param names to snake_case for Python function parameters (e.g. `pageSize` → `page_size`).

---

## How to add a new endpoint

1. Confirm the endpoint exists in the remote OpenAPI spec. If not, request a spec update first.
2. Run `make openapi`. Verify the new model class(es) appear in `src/main/@generated/openapi_models/models/`.
3. Register the operationId prefix in `VersionedResolver._ROUTES` (`event_resolver/resolver.py`).
4. Create a controller function in `event_resolver/controllers/<version>_<resource>_controller.py`.
   - Function name must **exactly** match the operationId.
   - Return `result.to_dict()` — never return model objects directly.
5. Create a service function in `event_resolver/service/`.
   - No HTTP details. No SPARQL calls. Pagination math lives here.
   - Enforce `MAX_PAGE_SIZE = 100` before any SPARQL call.
6. If reading from Wikidata, create SPARQL functions in `event_resolver/persistence/repository/`.
   - One COUNT function for pagination, one paginated SELECT function.
   - Set `agent=SPARQL_USER_AGENT` and `.setTimeout(SPARQL_TIMEOUT_SECONDS)` on every `SPARQLWrapper` instance.
   - Validate all user input before string-interpolating into SPARQL (see Security section below).
7. If the response shape is new, create a mapper in `event_resolver/mapper/`.
   - Input: SPARQL binding dict. Output: generated model instance.
   - Name the function `map_binding`, not `map` (avoids shadowing the Python builtin).
8. Write tests:
   - Unit tests in `src/test/python/unit/test_<module>.py` — mock the storage layer.
   - Integration tests in `src/test/python/test_events/test_<resource>_controller.py` — use starlette `TestClient` (`.get()`, `.post()`, etc.), mock the storage layer.
   - No test may make a real network call.
   - Every integration test class touching `/v2/*` routes must include `test_v1_events_still_works()`.
9. Run `make test` — all tests must pass.
10. Run `make lint` and `make format` — all style checks must pass.

---

## SPARQL result → model pipeline

```
HTTP request
    → connexion validates parameters against openapi.yaml
    → VersionedResolver routes operationId → controller function
    → controller calls service
        → service calls count_*(filters)            # COUNT query → int (for pagination)
        → service calls get_*_dao(filters, page, page_size)  # SELECT → list[dict]
        → service calls mapper for each binding dict
            {"item": {"value": "..."}, "itemLabel": {"value": "..."}, ...}
            → generated model instance (e.g. EventEvent)
        → Pagination model constructed
        → response body model constructed (e.g. EventEventListResponseBody)
    → controller calls .to_dict()                   # camelCase keys via attribute_map
    → connexion serialises to JSON
HTTP 200 response
```

---

## Pagination pattern

Every paginated endpoint uses two SPARQL queries:

```python
total_items   = count_*(filters)
offset        = (page - 1) * page_size
bindings      = get_*_dao(filters, page, page_size)
total_pages   = math.ceil(total_items / page_size)
has_next_page = page < total_pages
```

JSON response shape:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 142,
    "totalPages": 8,
    "hasNextPage": true
  }
}
```

---

## Filter injection pattern

| Parameter | Injection mechanism |
|---|---|
| `types` | `VALUES ?itemType { wd:Q... }` via `WikidataClassEnum.to_sparql_values_block()` |
| `regions` | Q-codes from `get_country_qcodes_for_regions()`, then `VALUES ?regionCountry { wd:Q... } ?item wdt:P17 ?regionCountry.` |
| `countries` | ISO alpha-3 validated → `VALUES ?iso3Code { "GBR" } ?isoCountry wdt:P298 ?iso3Code. ?item wdt:P17 ?isoCountry.` |
| `timeslot_start` / `timeslot_end` | `FILTER(?startTime >= "..."^^xsd:dateTime)` |
| (no dates) | Default: 30 days before today through 30 days after today, computed at call time via `_default_date_range()` |

When both `regions` and `countries` are provided, combine with `UNION` (OR semantics).

---

## Testing conventions

Mock at the **usage site** — always patch the name as it is bound in the module under test, not where it is defined:

```python
# Correct: patch the name as bound in the service module
patch("event_resolver.service.events_v2_service.count_events_v2", return_value=5)

# Wrong: patching the storage module after the service has already imported the name
patch("event_resolver.persistence.repository.events_v2_storage.count_events_v2", ...)
```

Integration tests use connexion's starlette `TestClient` — **not** `flask_testing.TestCase`. connexion 3.x is ASGI and incompatible with flask_testing.

---

## Toolchain

| Tool | Config location | Command | Excludes |
|---|---|---|---|
| **ruff** | `pyproject.toml [tool.ruff]` | `make lint` / `make format` | `src/main/@generated/` |
| **black** | `pyproject.toml [tool.black]` | `make format` | `src/main/@generated/` |
| **mypy** | `pyproject.toml [tool.mypy]` | `make typecheck` | `src/main/@generated/` |
| **pre-commit** | `.pre-commit-config.yaml` | runs on `git commit` | `src/main/@generated/` |
| **pytest** | `pyproject.toml [tool.pytest.ini_options]` | `make test` | — |
| **openapi-generator-cli** | `scripts/openapi.sh` | `make openapi` | — |

Pre-commit hook order: **gitleaks** (secrets) → **ruff** (lint + fix) → **black** (format) → **mypy** (types).

**All code — including AI-generated code — must pass pre-commit hooks before committing. Never use `--no-verify`.**

---

## Managing dependencies

`Pipfile` is the authoritative dependency specification. `Pipfile.lock` is the lockfile. `requirements.txt` is **auto-generated** from `Pipfile.lock` by the pre-commit hook — never edit it by hand.

```bash
# Add a runtime dependency:
pipenv install <package>

# Add a dev-only dependency (tools, test libs):
pipenv install --dev <package>

# Commit Pipfile and Pipfile.lock — requirements.txt regenerates automatically on the next commit

# Update all dependencies to latest allowed versions:
pipenv update
# Review Pipfile.lock diff before committing
```

---

## Security constraints

| Input | Validation |
|---|---|
| ISO 3166-1 alpha-3 country codes | `re.match(r"^[A-Z]{3}$", iso)` — raises `ValueError` if invalid |
| Country code search term (`q=`) | `_sanitize_search_term()` in `metadata_storage.py` — allows `[\w\s\-]` only |
| All other SPARQL parameters | Injected via `VALUES` blocks or `FILTER` with typed literals — no free-form string injection |

Never inject unvalidated user input into SPARQL query strings.

---

## Known constraints

| Constraint | Detail |
|---|---|
| `INTERNATION_ORGANIZATION` enum typo | Do NOT rename — API string `INTERNATIONAL_ORGANISATION` is bridged via `API_TO_WIKIDATA_ENUM` in `wikidata_class_enum.py` |
| `SOURCES_OF_INTERNATIONAL_LAW` vs `SOURCE_OF_INTERNATIONAL_LAW` | Enum member is plural; API string is singular. Resolved by `API_TO_WIKIDATA_ENUM`. |
| `page_size` cap | `MAX_PAGE_SIZE = 100` enforced in every service function before any SPARQL call |
| Date computation | Compute defaults inside the function via `_default_date_range()`, never at module import time |
| `map` as function name | Use `map_binding`, not `map`, to avoid shadowing the Python builtin |
| `pythonic_params=True` | connexion converts camelCase query param names to snake_case for Python function parameters |
| `base_model.py` camelCase fix | `to_dict()` uses `attribute_map` for JSON keys. Applied by `openapi.sh` — do not hand-revert. |
| OpenAPI spec URL | Pin to a specific commit SHA in `scripts/openapi.sh` — never use `main` |
| `@generated` is off-limits | Never edit by hand. Run `make openapi` to regenerate. |
| Wikidata SPARQL rate limits | Keep `LIMIT` ≤ 1000; set `SPARQL_USER_AGENT` and `SPARQL_TIMEOUT_SECONDS` on every call |
