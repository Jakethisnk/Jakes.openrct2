"""Data model describing an OpenRCT2 park."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Finances:
    cash: int = 0
    loan: int = 0
    max_loan: int = 0
    monthly_income: int = 0
    monthly_expenses: int = 0


@dataclass
class Guests:
    count: int = 0
    satisfaction: float = 100.0  # average happiness, 0-100
    park_rating: int = 0  # 0-999
    hungry_pct: float = 0.0
    thirsty_pct: float = 0.0
    needs_toilet_pct: float = 0.0


@dataclass
class Ride:
    name: str
    kind: str = "ride"
    excitement: float = 0.0
    breakdowns: int = 0
    days_since_inspection: int = 0
    breakdown_now: bool = False
    queue_length: int = 0


@dataclass
class Staff:
    handymen: int = 0
    mechanics: int = 0
    entertainers: int = 0
    security: int = 0


@dataclass
class Scenery:
    trees: int = 0
    benches: int = 0
    bins: int = 0
    litter_count: int = 0
    vandalism_count: int = 0


@dataclass
class ParkState:
    name: str = "Unnamed Park"
    finances: Finances = field(default_factory=Finances)
    guests: Guests = field(default_factory=Guests)
    rides: List[Ride] = field(default_factory=list)
    staff: Staff = field(default_factory=Staff)
    scenery: Scenery = field(default_factory=Scenery)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ParkState":
        return cls(
            name=data.get("name", "Unnamed Park"),
            finances=Finances(**data.get("finances", {})),
            guests=Guests(**data.get("guests", {})),
            rides=[Ride(**r) for r in data.get("rides", [])],
            staff=Staff(**data.get("staff", {})),
            scenery=Scenery(**data.get("scenery", {})),
        )
