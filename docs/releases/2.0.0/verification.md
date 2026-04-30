# Release 2.0.0 — Verification Report

> **Verified by:** Claude Code (claude-sonnet-4-6)
> **Date:** 2026-04-30
> **Branch:** `fix-cors`
> **Plan:** `docs/releases/2.0.0/plan.md`
> **Verdict: RELEASE READY** — all 7 planned steps implemented; deviations are corrections or improvements, not regressions.

---

## Step-by-step verification

### STEP 1 — Update the pinned spec SHA and regenerate models

**Status: COMPLIANT (with unplanned model renames handled per plan guidance)**

`config.env` contains `SPEC_SHA=c7d0fed479f9c477682619b8d44b65966e0adbf0` ✓

`python3 -c "import openapi_models.models"` succeeds with no import errors ✓

The new spec introduced a breaking rename across all v2 event model classes:

| Old class (SHA `775b07...`) | New class (SHA `c7d0fe...`) |
|---|---|
| `EventEvent` | `Event` |
| `EventEventListResponseBody` | `EventListResponseBody` |
| `EventEventType` | `EventType` |
| `EventEventTimeStateRelativeToNow` | `EventTimeStateRelativeToNow` |

The plan's STEP 1 inspection guidance correctly anticipated this possibility and instructed updating mapper/service imports if needed. The following files were updated accordingly:

- `src/main/event_resolver/mapper/event_v2_mapper.py` — import and return type updated to `Event`
- `src/main/event_resolver/service/events_v2_service.py` — import and all references updated to `EventListResponseBody`

**Addition beyond plan:** The new spec also introduced a `Region` model (`region.py`) — a string-constant class for region codes. The mapper's existing `list[str]` for regions required no change.

---

### STEP 2 — Remove the v1/events source stack

**Status: COMPLIANT**

All six files are deleted:

| File | Deleted |
|---|---|
| `src/main/event_resolver/controllers/events_controller.py` | ✓ |
| `src/main/event_resolver/service/events_service.py` | ✓ |
| `src/main/event_resolver/persistence/repository/events_storage.py` | ✓ |
| `src/main/event_resolver/mapper/event_mapper.py` | ✓ |
| `src/main/event_resolver/persistence/models/wikidata_class_name.py` | ✓ |
| `src/main/event_resolver/encoder.py` | ✓ |

`src/main/event_resolver/resolver.py` — `v1_events_` entry removed from `_ROUTES` and from the docstring. The table now contains exactly two entries:

```python
_ROUTES = [
    ("v2_events_",   "event_resolver.controllers.events_v2_controller"),
    ("v2_metadata_", "event_resolver.controllers.events_v2_metadata_controller"),
]
```

---

### STEP 3 — Remove v1 tests and update the resolver unit tests

**Status: COMPLIANT**

`src/test/python/test_events/test_events_controller.py` — deleted ✓

`src/test/python/unit/test_resolver.py` — retains exactly the four methods specified by the plan:

| Method | Status |
|---|---|
| `test_routes_v2_events_to_events_v2_controller` | ✓ present |
| `test_routes_v2_metadata_to_events_v2_metadata_controller` | ✓ present |
| `test_raises_for_unknown_operation` | ✓ present |
| `test_raises_when_function_missing_from_module` | ✓ updated to `"v2_events_get"` |
| `test_routes_v1_events_to_events_controller` | ✓ deleted |

`src/test/python/test_events/test_events_v2_controller.py` — `test_v1_events_still_works` deleted ✓

---

### STEP 4 — Add CORS middleware to `__main__.py`

**Status: COMPLIANT**

`src/main/__main__.py`:

- `from starlette.middleware.cors import CORSMiddleware` imported at module level ✓
- `CORS_ALLOWED_ORIGINS` read from environment, split on commas, stripped; falls back to `["*"]` when absent or empty ✓
- `CORSMiddleware` registered at `MiddlewarePosition.BEFORE_ROUTING` ✓
- `allow_methods=["*"]`, `allow_headers=["*"]` ✓
- `StripEmptyArrayParams` remains at `BEFORE_VALIDATION` (inner) ✓
- Final middleware order matches the plan exactly ✓

---

### STEP 5 — Document `CORS_ALLOWED_ORIGINS` in `config.env`

**Status: COMPLIANT**

`config.env` contains both `SPEC_SHA` (updated) and `CORS_ALLOWED_ORIGINS=` with a four-line comment block explaining the comma-separated format, the production guidance (set to exact frontend origin), and the local-dev default (`*`) ✓

---

### STEP 6 — Write CORS integration tests

**Status: COMPLIANT (with corrected test client API)**

`src/test/python/test_events/test_cors.py` is present with all three tests:

| Test | Result |
|---|---|
| `test_get_request_has_allow_origin_header` | PASSED ✓ |
| `test_options_preflight_returns_200` | PASSED ✓ |
| `test_options_preflight_has_allow_origin_header` | PASSED ✓ |

**Deviation — test client method calls:** The plan's STEP 6 code snippet used `self.client.open("/path", method="GET", ...)` and `self.client.open("/path", method="OPTIONS", ...)`. connexion 3.x's `FlaskApp.test_client()` returns a starlette `TestClient` (requests-based), which exposes method-specific calls (`.get()`, `.options()`, etc.) and has no `.open()` method. The actual implementation uses `.client.get()` and `.client.options()` — the correct API for this test client.

**Addition beyond plan:** `src/test/python/test_events/__init__.py` `_make_connexion_app()` was updated to register `CORSMiddleware` at `BEFORE_ROUTING`. The plan only specified changes to `__main__.py` and `test_cors.py`. Without this addition the test app would have been missing the middleware and all three CORS tests would have failed.

---

### STEP 7 — Bump the application version

**Status: COMPLIANT**

`pyproject.toml` `[project]` table: `version = "2.0.0"` ✓

---

## Test suite result

```
95 passed, 3 warnings in 3.15s
```

All 95 tests pass on branch `fix-cors`. The 3 new CORS tests are included in this count.

---

## Deviation summary

| # | Item | Plan | Implementation | Classification |
|---|---|---|---|---|
| D1 | v2 model class names | Not anticipated (plan said "inspect and update if needed") | `EventEvent*` → `Event*` rename throughout; mapper and service imports updated | Handled per STEP 1 guidance — not a regression |
| D2 | `test_cors.py` test client API | `self.client.open(method="GET/OPTIONS")` | `self.client.get()` / `self.client.options()` | Correction — starlette `TestClient` has no `.open()` method |
| D3 | `test_events/__init__.py` | Not mentioned | `CORSMiddleware` added to `_make_connexion_app()` | Required for CORS tests to function; omission in plan |

---

## Backward compatibility

`/v1/events` is intentionally removed. All `/v2/*` endpoints (`/v2/events`, `/v2/metadata/event-types`, `/v2/metadata/regions`, `/v2/metadata/country-codes`) continue to work unchanged, verified by the full integration test suite.

---

## Overall verdict

**RELEASE READY.** All 7 steps from `docs/releases/2.0.0/plan.md` are implemented on branch `fix-cors`. The CORS fix resolves the `CORS Missing Allow Origin` browser error. The `/v1/events` stack is fully removed. The OpenAPI spec is advanced to SHA `c7d0fed`. The application version is `2.0.0`. All 95 tests pass.
