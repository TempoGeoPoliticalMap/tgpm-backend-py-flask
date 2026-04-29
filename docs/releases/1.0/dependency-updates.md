# Dependency Updates — Release 1.0

This document records the dependency audit performed for release 1.0 (2026-04-23).

## Policy

`Pipfile` is the authoritative dependency specification (loose `>=` constraints).
`Pipfile.lock` is the lockfile — commit it together with `Pipfile` changes.
`requirements.txt` is auto-generated from `Pipfile.lock` by the pre-commit hook — never edit it by hand.

## Audit table

| Package | Pre-1.0 version | Release 1.0 target | Notes |
|---|---|---|---|
| connexion | 3.1.0 | ^3.3.0 | Upgraded; now using `FlaskApp` (ASGI). `flask_testing.TestCase` incompatible — replaced with starlette `TestClient`. |
| Flask | 3.0.3 | ^3.1.3 | Minor upgrade. |
| uvicorn | 0.32.0 | ^0.46.0 | Minor upgrade. |
| pydantic | 2.9.2 | ^2.13.3 | Minor upgrade. |
| SPARQLWrapper | 2.0.0 | ^2.0.0 | No change. |
| requests | 2.32.3 | ^2.33.1 | Minor upgrade. |
| python-dateutil | 2.9.0.post0 | ^2.9.0 | No change. |
| PyYAML | 6.0.2 | ^6.0.3 | Patch upgrade. |
| rdflib | 7.1.1 | ^7.6.0 | Minor upgrade. |
| starlette | 0.41.2 | ^1.0.0 | Major upgrade (1.x). Must remain compatible with uvicorn version. |
| jsonschema | 4.23.0 | ^4.26.0 | Minor upgrade. `RefResolver` deprecation warnings present — will be resolved in a future release. |
| httpx | 0.27.2 | ^0.28.1 | Minor upgrade. Used by connexion test client. |
| swagger-ui-bundle | 1.1.0 | ^1.1.0 | No change. |
| Werkzeug | 3.1.2 | ^3.1.8 | Patch upgrade. |
| Jinja2 | 3.1.4 | ^3.1.6 | Patch upgrade. |

## New additions

| Package | Version | Reason |
|---|---|---|
| `connexion[flask]` extra | — | Required for `a2wsgi` ASGI→WSGI bridge used by connexion FlaskApp |
| `black` | — | Code formatter; used in `scripts/openapi.sh` post-processing step |

## Known deprecation warnings

`jsonschema.RefResolver` is deprecated as of jsonschema 4.18.0. The warning originates
inside connexion internals (`connexion/json_schema.py`). It does not affect runtime
behaviour; it will be resolved when connexion updates its internal validation logic.

## Upgrade process

To update dependencies in a future release:

```bash
# Update all packages to latest allowed versions:
pipenv update

# Or update a specific package:
pipenv install <package>==<new-version>

# Verify imports:
pipenv run python -c "import connexion, flask, uvicorn, pydantic, SPARQLWrapper"

# Run full test suite:
make test
```

Commit `Pipfile` and `Pipfile.lock`. The `requirements.txt` regenerates automatically on the next commit via the pre-commit hook.
