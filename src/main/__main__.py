#!/usr/bin/env python3
import sys
from pathlib import Path
import connexion
import uvicorn
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound

from event_resolver.resolver import VersionedResolver

root_path = Path(sys.path[0]).resolve()


def main():
    app = connexion.AsyncApp(
        __name__, specification_dir="./@generated/openapi_models/openapi"
    )

    @app.app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.app.errorhandler(EndPointInternalError)
    @app.app.errorhandler(EndPointNotFound)
    def handle_sparql_error(exc):
        return {"detail": "Upstream data source unavailable"}, 502

    app.add_api(
        "openapi.yaml",
        arguments={"title": "TempoGeoPoliticalMap RESTful API"},
        pythonic_params=True,
        resolver=VersionedResolver(),
    )

    uvicorn.run(app, port=8080)


if __name__ == "__main__":
    main()
