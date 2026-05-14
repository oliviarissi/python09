#!/usr/bin/env python3

from typing import Optional
from datetime import datetime

try:
    from pydantic import BaseModel, Field, ValidationError  # type: ignore[import-not-found]
except ModuleNotFoundError as e:
    raise SystemExit(
        "Script requires pydantic. Install it with: pip install pydantic"
    ) from e


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def print_station(station: SpaceStation) -> None:
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status {'Operational' if station.is_operational else 'Offline'}\n")


def main() -> None:

    print("Space Station Data Validation")
    print("=" * 40)

    try:
        station_valid = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-05-10T14:30:00"
        )
        print_station(station_valid)
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))

    print("=" * 40)

    try:
        station_invalid = SpaceStation(
            station_id="BAD001",
            name="Broken Space Station",
            crew_size=22,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-05-10T14:30:00",
            is_operational=True,
        )
        print_station(station_invalid)
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()
