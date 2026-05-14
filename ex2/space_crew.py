#!/usr/bin/env python3

from enum import Enum
from typing import List
from datetime import datetime

try:
    from pydantic import BaseModel, Field, ValidationError, model_validator  # type: ignore[import-not-found]
except ModuleNotFoundError as e:
    raise SystemExit(
        "Script requires pydantic. Install it with: pip install pydantic"
    ) from e


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(
            c.rank in (Rank.commander, Rank.captain)
            for c in self.crew
        ):
            raise ValueError("Must have at least one Commander or Captain")
        if self.duration_days > 365:
            experienced = sum(c.years_experience >= 5 for c in self.crew)
            if experienced < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% "
                    "experienced crew (5+ years)"
                )
        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")
        return self


def print_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )
    print()


def main() -> None:

    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2026-01-10T10:00:00",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C01",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=40,
                    specialization="Mission Command",
                    years_experience=15,
                ),
                CrewMember(
                    member_id="C02",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=32,
                    specialization="Navigation",
                    years_experience=6,
                ),
                CrewMember(
                    member_id="C03",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=28,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ],
        )
        print_mission(valid_mission)

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    print("=" * 40)

    try:
        invalid_mission = SpaceMission(
            mission_id="X999_FAIL",
            mission_name="Broken Mission",
            destination="Mars",
            launch_date="2026-01-10T10:00:00",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C01",
                    name="Bob",
                    rank=Rank.lieutenant,
                    age=30,
                    specialization="Engineering",
                    years_experience=2,
                ),
                CrewMember(
                    member_id="C02",
                    name="Alice",
                    rank=Rank.officer,
                    age=28,
                    specialization="Science",
                    years_experience=1,
                ),
            ],
        )
        print_mission(invalid_mission)

    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
