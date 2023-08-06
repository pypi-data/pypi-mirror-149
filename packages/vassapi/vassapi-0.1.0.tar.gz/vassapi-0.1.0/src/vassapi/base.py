"""Client base class that handles authentication and httpx."""

from typing import Any, Optional

import httpx

from .const import DEFAULT_PORT
from .exceptions import handle_error


class BaseClient:
    """Base client that handles authentication and requests."""

    def __init__(
        self,
        host: str,
        token: str,
        port: Optional[int] = None,
    ):
        """Initialize base client."""
        port = port or DEFAULT_PORT
        self._url = f"http://{host}:{port}/api"
        self._headers = {"token": token}

    def request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send synchronous request."""
        response = httpx.request(
            method=method,
            url=f"{self._url}{endpoint}",
            headers=self._headers,
            **kwargs,
        )
        handle_error(response)
        return response

    async def async_request(self, method: str, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send asynchronous request."""
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=f"{self._url}{endpoint}",
                headers=self._headers,
                **kwargs,
            )
            handle_error(response)
            return response

    def get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send synchronous GET request."""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send synchronous POST request."""
        return self.request("POST", endpoint, **kwargs)

    async def async_get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send asynchronous GET request."""
        return await self.async_request("GET", endpoint, **kwargs)

    async def async_post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Send asynchronous POST request."""
        return await self.async_request("POST", endpoint, **kwargs)


__all__ = ["BaseClient"]
