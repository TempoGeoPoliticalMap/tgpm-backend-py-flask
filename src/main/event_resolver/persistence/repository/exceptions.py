class UpstreamTimeoutError(TimeoutError):
    pass


class UpstreamRateLimitError(Exception):
    def __init__(self, message: str, retry_after: str | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class UpstreamUnavailableError(Exception):
    pass
