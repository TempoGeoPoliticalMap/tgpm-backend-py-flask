import logging
import os
import unittest

import connexion
from connexion.middleware import MiddlewarePosition

from event_resolver.middleware import StripEmptyArrayParams
from event_resolver.resolver import VersionedResolver

_SPEC_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "..", "..",
        "src", "main", "@generated", "openapi_models", "openapi",
    )
)


def _make_connexion_app():
    logging.getLogger("connexion.operation").setLevel("ERROR")
    app = connexion.FlaskApp(
        __name__,
        specification_dir=_SPEC_DIR,
    )
    app.add_middleware(StripEmptyArrayParams, position=MiddlewarePosition.BEFORE_VALIDATION)
    app.add_api(
        "openapi.yaml",
        pythonic_params=True,
        resolver=VersionedResolver(),
    )
    return app


class BaseTestCase(unittest.TestCase):
    """Base integration test case using connexion's ASGI test client."""

    _connexion_app = None

    @classmethod
    def setUpClass(cls):
        if cls._connexion_app is None:
            cls._connexion_app = _make_connexion_app()

    def setUp(self):
        self._client_ctx = self._connexion_app.test_client()
        self.client = self._client_ctx.__enter__()

    def tearDown(self):
        self._client_ctx.__exit__(None, None, None)

    def assert200(self, response, message=None):
        self.assertEqual(response.status_code, 200, message or response.text)

    def assert400(self, response, message=None):
        self.assertEqual(response.status_code, 400, message or response.text)

    def assert404(self, response, message=None):
        self.assertEqual(response.status_code, 404, message or response.text)
