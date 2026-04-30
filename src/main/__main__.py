#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import json

import connexion
import uvicorn
import yaml
from flask import redirect
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound
from starlette.middleware.cors import CORSMiddleware

from connexion.middleware import MiddlewarePosition

from event_resolver.middleware import StripEmptyArrayParams
from event_resolver.persistence.repository.exceptions import (
    UpstreamRateLimitError,
    UpstreamUnavailableError,
)
from event_resolver.resolver import VersionedResolver

root_path = Path(sys.path[0]).resolve()


def main():
    app = connexion.FlaskApp(
        __name__, specification_dir="./@generated/openapi_models/openapi"
    )

    app.add_middleware(StripEmptyArrayParams, position=MiddlewarePosition.BEFORE_VALIDATION)

    _raw_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
    allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()] or ["*"]
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_ROUTING,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.app.route("/")
    def root_redirect():
        return redirect("/ui")

    @app.app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.app.route("/swagger")
    @app.app.route("/swagger/")
    def swagger_redirect():
        return redirect("/ui")

    @app.app.route("/.well-known/openapi")
    def well_known_openapi():
        spec_path = root_path / "@generated/openapi_models/openapi/openapi.yaml"
        spec = yaml.safe_load(spec_path.read_text())
        return app.app.response_class(
            json.dumps(spec),
            mimetype="application/vnd.oai.openapi+json;version=3.0",
        )

    @app.app.errorhandler(EndPointInternalError)
    @app.app.errorhandler(EndPointNotFound)
    def handle_sparql_error(exc):
        return {"detail": "Upstream data source unavailable"}, 502

    @app.app.errorhandler(TimeoutError)
    def handle_sparql_timeout(exc):
        return {"detail": "Upstream data source timeout"}, 504

    @app.app.errorhandler(UpstreamRateLimitError)
    def handle_sparql_rate_limit(exc):
        headers = {}
        if exc.retry_after:
            headers["Retry-After"] = exc.retry_after
        return {"detail": "Upstream data source rate limited"}, 429, headers

    @app.app.errorhandler(UpstreamUnavailableError)
    def handle_sparql_unavailable(exc):
        return {"detail": "Upstream data source unavailable"}, 502

    app.add_api(
        "openapi.yaml",
        arguments={"title": "TempoGeoPoliticalMap RESTful API"},
        pythonic_params=True,
        resolver=VersionedResolver(),
    )

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
