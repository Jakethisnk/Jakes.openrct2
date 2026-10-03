"""Park state sources. Add a new loader here to read real OpenRCT2 data."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from .park import ParkState

MOCK_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class ParkStateSource(Protocol):
    def load(self) -> ParkState: ...


class JsonFileSource:
    def __init__(self, path: Path | str):
        self.path = Path(path)

    def load(self) -> ParkState:
        with open(self.path, encoding="utf-8") as f:
            return ParkState.from_dict(json.load(f))


class MockSource(JsonFileSource):
    def __init__(self, name: str = "struggling_park"):
        super().__init__(MOCK_DATA_DIR / f"{name}.json")
