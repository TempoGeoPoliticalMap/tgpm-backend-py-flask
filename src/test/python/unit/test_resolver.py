import unittest
from unittest.mock import MagicMock, patch

from event_resolver.resolver import VersionedResolver


class TestVersionedResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = VersionedResolver()

    def test_routes_v2_events_to_events_v2_controller(self):
        with patch("event_resolver.resolver.importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_module.v2_events_get = lambda: None
            mock_import.return_value = mock_module
            self.resolver.resolve_function_from_operation_id("v2_events_get")
            mock_import.assert_called_with("event_resolver.controllers.events_v2_controller")

    def test_routes_v2_metadata_to_events_v2_metadata_controller(self):
        with patch("event_resolver.resolver.importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_module.v2_metadata_event_types_get = lambda: None
            mock_import.return_value = mock_module
            self.resolver.resolve_function_from_operation_id("v2_metadata_event_types_get")
            mock_import.assert_called_with("event_resolver.controllers.events_v2_metadata_controller")

    def test_raises_for_unknown_operation(self):
        with self.assertRaises(ValueError):
            self.resolver.resolve_function_from_operation_id("unknown_operation_get")

    def test_raises_when_function_missing_from_module(self):
        with patch("event_resolver.resolver.importlib.import_module") as mock_import:
            mock_module = MagicMock(spec=[])  # no attributes
            mock_import.return_value = mock_module
            with self.assertRaises((ValueError, AttributeError)):
                self.resolver.resolve_function_from_operation_id("v2_events_get")
