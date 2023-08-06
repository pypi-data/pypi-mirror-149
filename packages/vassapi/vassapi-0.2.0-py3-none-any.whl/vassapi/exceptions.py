"""Host client custom errors."""

import httpx


class HTTPError(Exception):
    """Base HTTP error."""


class ClientError(HTTPError):
    """4xx - Client error."""


class ServerError(HTTPError):
    """5xx - Server error."""


def handle_error(response: httpx.Response) -> None:
    """Raise error based on response return code."""
    if response.is_success:
        return

    if response.is_client_error:
        raise ClientError(response.reason_phrase)

    if response.is_server_error:
        raise ServerError(response.reason_phrase)
