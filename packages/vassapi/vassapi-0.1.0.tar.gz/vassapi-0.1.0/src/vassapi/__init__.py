"""Voice Assistant Python client."""

from functools import lru_cache
from typing import Any, Optional

import httpx

from .base import BaseClient
from .const import STATUS_ACTIVE, TIMEOUT, Endpoint
from .models import DeviceInfo, States


class CoreClient(BaseClient):
    """Synchronous client with core functionality."""

    def is_running(self) -> bool:
        try:
            return self.get(Endpoint.STATUS, timeout=TIMEOUT).text == STATUS_ACTIVE  # type: ignore
        except httpx.ReadTimeout:
            return False

    def trigger(self) -> None:
        """Trigger Voice Assistant."""
        self.get(Endpoint.TRIGGER)

    def reload(self) -> None:
        """Reload Voice Assistant."""
        self.get(Endpoint.RELOAD)

    def say(self, message: str, cache: bool = False) -> None:
        """Perform text to speech."""
        self.post(Endpoint.SAY, json={"text": message, "cache": cache})

    def skills(self) -> list[str]:
        """Get list of current skill names."""
        return self.get(Endpoint.SKILLS).json()  # type: ignore

    def run_skill(self, name: str, entities: Optional[dict] = None) -> None:
        """Run skills."""
        self.get(Endpoint.SKILLS, json={"name": name, "entities": entities or {}})

    def config(self) -> dict:
        """Get Voice Assistant's config."""
        return self.get(Endpoint.CONFIG).json()  # type: ignore

    def set_config(self, config: dict) -> None:
        """Set Voice Assistant's config."""
        self.post(Endpoint.CONFIG, json=config)

    @lru_cache
    def device_info(self) -> DeviceInfo:
        """Get host device info."""
        info = self.get(Endpoint.INFO).json()
        return DeviceInfo.from_dict(info)

    def states(self) -> States:
        """Get Voice Assistant's states."""
        states = self.get(Endpoint.STATES).json()
        return States.from_dict(states)

    def set_state(self, attribute: str, value: Any) -> None:
        """Set state of an attribute."""
        self.post(Endpoint.STATES, json={attribute: value})


class AsyncCoreClient(BaseClient):
    """Asynchronous client with core functionality."""

    async def async_is_running(self) -> bool:
        try:
            r = await self.async_get(Endpoint.STATUS, timeout=TIMEOUT)
            return r.text == STATUS_ACTIVE  # type: ignore
        except httpx.ReadTimeout:
            return False

    async def async_trigger(self) -> None:
        """Trigger Voice Assistant."""
        await self.async_get(Endpoint.TRIGGER)

    async def async_reload(self) -> None:
        """Reload Voice Assistant."""
        await self.async_get(Endpoint.RELOAD)

    async def async_say(self, message: str, cache: bool = False) -> None:
        """Perform text to speech."""
        await self.async_post(Endpoint.SAY, json={"text": message, "cache": cache})

    async def async_skills(self) -> list[str]:
        """Get list of current skill names."""
        r = await self.async_get(Endpoint.SKILLS)
        return r.json()  # type: ignore

    async def async_run_skill(self, name: str, entities: Optional[dict] = None) -> None:
        """Run skills."""
        await self.async_get(Endpoint.SKILLS, json={"name": name, "entities": entities or {}})

    async def async_config(self) -> dict:
        """Get Voice Assistant's config."""
        r = await self.async_get(Endpoint.CONFIG)
        return r.json()  # type: ignore

    async def async_set_config(self, config: dict) -> None:
        """Set Voice Assistant's config."""
        await self.async_post(Endpoint.CONFIG, json=config)

    async def async_device_info(self) -> DeviceInfo:
        """Get host device info."""
        r = await self.async_get(Endpoint.INFO)
        return DeviceInfo.from_dict(r.json())

    async def async_states(self) -> States:
        """Get Voice Assistant's states."""
        r = await self.async_get(Endpoint.STATES)
        return States.from_dict(r.json())

    async def async_set_state(self, attribute: str, value: Any) -> None:
        """Set state of an attribute."""
        await self.async_post(Endpoint.STATES, json={attribute: value})


class ExtendedClient(CoreClient):
    """Synchronous client with extended functionality."""

    def set_input_mute(self, mute: bool) -> None:
        """Enable or disable microphone."""
        self.set_state("input_muted", mute)

    def set_output_mute(self, mute: bool) -> None:
        """Set volume mute of host device."""
        self.set_state("output_muted", mute)

    def set_output_volume(self, level: int) -> None:
        """Set volume level of host device."""
        self.set_state("output_volume", level)


class AsyncExtendedClient(AsyncCoreClient):
    """Asynchronous client with extended functionality."""

    async def async_set_input_mute(self, mute: bool) -> None:
        """Enable or disable microphone."""
        await self.async_set_state("input_muted", mute)

    async def async_set_output_mute(self, mute: bool) -> None:
        """Set volume mute of host device."""
        await self.async_set_state("output_muted", mute)

    async def async_set_output_volume(self, level: int) -> None:
        """Set volume level of host device."""
        await self.async_set_state("output_volume", level)


class Client(ExtendedClient, AsyncExtendedClient):
    """Voice Assistant client."""


__all__ = ["Client", "DeviceInfo", "States"]
