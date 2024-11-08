#!/usr/bin/env python3
import sys
from pathlib import Path
import connexion
from connexion.resolver import RelativeResolver
import uvicorn

root_path = Path(sys.path[0]).resolve()

def main():
    app = connexion.AsyncApp(__name__, specification_dir="./@generated/openapi_models/openapi")
    app.add_api(
        "openapi.yaml",
        arguments={"title": "TempoGeoPoliticalMap RESTful API"},
        pythonic_params=True,
        resolver=RelativeResolver("event_resolver.controllers.events_controller"),
    )

    uvicorn.run(app, port=8080)


if __name__ == "__main__":
    main()
