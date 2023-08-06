"""Host data models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class States:
    """Respresent states of voice assistant device."""

    input_muted: bool
    output_muted: bool
    output_volume: int

    @classmethod
    def from_dict(cls, dictionary: dict) -> States:
        """Initiate instance from dictionary."""
        return cls(
            input_muted=dictionary["input_muted"],
            output_muted=dictionary["output_muted"],
            output_volume=dictionary["output_volume"],
        )


@dataclass
class DeviceInfo:
    """Represent info about voice assistant device."""

    name: str
    version: str
    uuid: str
    language: str
    area: str

    @classmethod
    def from_dict(cls, dictionary: dict) -> DeviceInfo:
        """Initiate instance from dictionary."""
        return cls(
            name=dictionary["name"],
            version=dictionary["version"],
            uuid=dictionary["uuid"],
            language=dictionary["language"],
            area=dictionary["area"],
        )
