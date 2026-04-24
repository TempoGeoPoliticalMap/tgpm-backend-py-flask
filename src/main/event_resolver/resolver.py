import importlib
from collections.abc import Callable

from connexion.resolver import Resolver


class VersionedResolver(Resolver):
    """Routes connexion operations to controller modules based on operation-ID prefix.

    Routing rules (first match wins — order matters):
      "v1_events_"   → event_resolver.controllers.events_controller
      "v2_events_"   → event_resolver.controllers.events_v2_controller
      "v2_metadata_" → event_resolver.controllers.events_v2_metadata_controller

    Resolved functions are cached after first lookup so importlib is not
    re-invoked on every request.
    """

    _ROUTES = [
        ("v1_events_", "event_resolver.controllers.events_controller"),
        ("v2_events_", "event_resolver.controllers.events_v2_controller"),
        ("v2_metadata_", "event_resolver.controllers.events_v2_metadata_controller"),
    ]

    def __init__(self):
        super().__init__()
        self._cache: dict[str, Callable] = {}

    def resolve_operation_id(self, operation) -> str:
        """Return the bare operationId, ignoring x-openapi-router-controller."""
        return operation.operation_id

    def resolve_function_from_operation_id(self, operation_id: str) -> Callable:
        if operation_id in self._cache:
            return self._cache[operation_id]
        for prefix, module_path in self._ROUTES:
            if operation_id.startswith(prefix):
                module = importlib.import_module(module_path)
                try:
                    fn = getattr(module, operation_id)
                except AttributeError:
                    raise ValueError(
                        f"Controller function '{operation_id}' not found in '{module_path}'"
                    )
                self._cache[operation_id] = fn
                return fn
        raise ValueError(f"No controller registered for operation: '{operation_id}'")
