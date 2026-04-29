from urllib.parse import parse_qs, urlencode

# Query parameters that carry comma-separated enum arrays.
# Sending ?types= (key present, value empty) is treated as "no filter".
_ARRAY_QUERY_PARAMS = frozenset({"types", "regions", "countries"})


class StripEmptyArrayParams:
    """ASGI middleware: removes empty-string items from array query params.

    Prevents connexion from receiving [""] when the client sends ?types=,
    which would fail enum validation even though the intent is "no filter".
    """

    def __init__(self, app):
        self._app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("query_string"):
            raw = scope["query_string"].decode()
            params = parse_qs(raw, keep_blank_values=True)
            cleaned = {}
            for k, vs in params.items():
                filtered = [v for v in vs if v] if k in _ARRAY_QUERY_PARAMS else vs
                if filtered:
                    cleaned[k] = filtered
            scope = {**scope, "query_string": urlencode(cleaned, doseq=True).encode()}
        await self._app(scope, receive, send)
