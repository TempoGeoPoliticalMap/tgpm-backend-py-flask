# Technical Design — TGPM Backend

This folder contains the living technical reference for the TGPM backend service.

**If you are an AI agent or a new engineer, start with [`/AGENTS.md`](../../AGENTS.md) at the repository root.** It is the single, complete onboarding guide — commands, layer rules, recipes, and constraints in one place.

## Contents

| File                                                                             | Purpose |
|----------------------------------------------------------------------------------|---|
| [architecture.md](architecture.md)                                               | Layer diagram, component responsibilities, data flow |
| [sparql-queries.md](sparql-queries.md)                                           | Full SPARQL templates used in `events_v2_storage.py` and `metadata_storage.py` |
| [wikidata-mappings.md](wikidata-mappings.md)                                     | Event-type Q-code table and region → country Q-code table |
| [../releases/1.0.0/dependency-updates.md](../releases/1.0.0/dependency-updates.md) | Dependency audit: previous pinned versions vs. release 1.0 targets |

## Spec URL

```
https://raw.githubusercontent.com/TempoGeoPoliticalMap/tgpm-openapi/<SPEC_SHA>/openapi.bundled.yaml
```

The pinned `SPEC_SHA` is recorded in `scripts/openapi.sh`. Always use the SHA-pinned URL — never `main`.
