def info_from_BearerAuth(token: str) -> dict:
    """Auth is handled at infrastructure level; this is a no-op pass-through."""
    return {"sub": "anonymous"}
