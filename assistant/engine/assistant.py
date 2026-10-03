from __future__ import annotations

from typing import List, Optional, Sequence

from ..logic.recommendation import Recommendation
from ..logic.rules import ALL_RULES, Rule
from ..state import ParkState


class Assistant:
    def __init__(self, rules: Optional[Sequence[Rule]] = None):
        self.rules = list(rules) if rules is not None else list(ALL_RULES)

    def analyze(self, park: ParkState) -> List[Recommendation]:
        recs = [r for rule in self.rules for r in rule(park)]
        return sorted(recs, key=lambda r: -r.priority)
