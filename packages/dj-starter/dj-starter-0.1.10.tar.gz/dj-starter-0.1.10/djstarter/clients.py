import logging

from httpx import Client, HTTPStatusError, TransportError

from djstarter import decorators

logger = logging.getLogger(__name__)

RETRY_EXCEPTIONS = (
    HTTPStatusError,
    TransportError
)


class RetryClient(Client):
    """
    Http/2 Client
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            follow_redirects=True,
            *args,
            **kwargs
        )

    @decorators.retry(retry_exceptions=RETRY_EXCEPTIONS)
    @decorators.api_error_check
    def send(self, *args, **kwargs):
        return super().send(*args, **kwargs)
