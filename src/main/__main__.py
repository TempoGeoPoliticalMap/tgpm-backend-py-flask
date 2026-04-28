#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import connexion
import uvicorn
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError, EndPointNotFound

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

    @app.app.route("/health")
    def health():
        return {"status": "ok"}, 200

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
