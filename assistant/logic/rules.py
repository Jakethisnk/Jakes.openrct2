"""Rule-based analysis. Each rule maps a ParkState to recommendations."""
from __future__ import annotations

from typing import Callable, List

from ..state import ParkState
from .recommendation import Priority, Recommendation

Rule = Callable[[ParkState], List[Recommendation]]


def finance_rules(p: ParkState) -> List[Recommendation]:
    f, out = p.finances, []
    if f.cash < 0:
        out.append(Recommendation("finance", Priority.HIGH,
                                  "You are in debt. Stop building and raise ride prices."))
    elif f.cash < 5000:
        out.append(Recommendation("finance", Priority.MEDIUM,
                                  "Cash is low. Avoid big purchases until income improves."))
    if f.monthly_expenses > f.monthly_income:
        out.append(Recommendation("finance", Priority.HIGH,
                                  "Park is losing money each month. Raise prices or cut staff/ride costs."))
    if f.loan > 0 and f.cash > f.loan * 2:
        out.append(Recommendation("finance", Priority.LOW,
                                  "You have spare cash; repay the loan to save interest."))
    return out


def guest_rules(p: ParkState) -> List[Recommendation]:
    g, out = p.guests, []
    if g.satisfaction < 50:
        out.append(Recommendation("guests", Priority.HIGH,
                                  "Guests are unhappy. Check ride prices, queues, and cleanliness."))
    elif g.satisfaction < 70:
        out.append(Recommendation("guests", Priority.MEDIUM,
                                  "Guest happiness is mediocre; add entertainment and scenery."))
    if g.park_rating and g.park_rating < 600:
        out.append(Recommendation("guests", Priority.MEDIUM,
                                  f"Park rating is {g.park_rating}; aim for 600+ to attract more guests."))
    if g.needs_toilet_pct > 15:
        out.append(Recommendation("guests", Priority.MEDIUM,
                                  "Many guests need a toilet. Build more restrooms."))
    if g.hungry_pct > 20:
        out.append(Recommendation("guests", Priority.MEDIUM, "Many guests are hungry. Add food stalls."))
    if g.thirsty_pct > 20:
        out.append(Recommendation("guests", Priority.MEDIUM, "Many guests are thirsty. Add drink stalls."))
    return out


def ride_rules(p: ParkState) -> List[Recommendation]:
    out = []
    for r in p.rides:
        if r.breakdown_now:
            out.append(Recommendation("rides", Priority.HIGH,
                                      f"{r.name} is broken down. Send a mechanic."))
        elif r.days_since_inspection > 30 or r.breakdowns >= 3:
            out.append(Recommendation("rides", Priority.MEDIUM,
                                      f"{r.name} needs maintenance (inspect more often)."))
        if r.queue_length > 50:
            out.append(Recommendation("rides", Priority.LOW,
                                      f"{r.name} has a long queue; lower its price or add capacity."))
    return out


def staff_rules(p: ParkState) -> List[Recommendation]:
    s, out = p.staff, []
    n_rides = len(p.rides)
    if n_rides and s.mechanics < max(1, n_rides // 4):
        out.append(Recommendation("staff", Priority.HIGH,
                                  f"Too few mechanics ({s.mechanics}) for {n_rides} rides. Hire more."))
    if p.guests.count and s.handymen < max(1, p.guests.count // 150):
        out.append(Recommendation("staff", Priority.MEDIUM, "Hire more handymen to sweep litter."))
    if p.guests.count > 200 and s.entertainers == 0:
        out.append(Recommendation("staff", Priority.LOW, "Hire entertainers to boost happiness."))
    if s.security == 0 and (p.scenery.vandalism_count > 0 or p.guests.count > 300):
        out.append(Recommendation("staff", Priority.MEDIUM, "Hire security guards to stop vandalism."))
    return out


def scenery_rules(p: ParkState) -> List[Recommendation]:
    sc, out = p.scenery, []
    guests = max(p.guests.count, 1)
    if sc.litter_count > guests / 10:
        out.append(Recommendation("scenery", Priority.MEDIUM,
                                  "Park is littered. Add bins and handymen."))
    if sc.bins < guests / 50:
        out.append(Recommendation("scenery", Priority.LOW, "Add more litter bins along paths."))
    if sc.benches < guests / 50:
        out.append(Recommendation("scenery", Priority.LOW, "Add benches for tired guests."))
    if sc.trees < len(p.rides) * 5:
        out.append(Recommendation("scenery", Priority.LOW, "Add trees and scenery to improve the park."))
    if sc.vandalism_count > 5:
        out.append(Recommendation("scenery", Priority.MEDIUM, "Vandalism is rising; repair and add security."))
    return out


ALL_RULES: List[Rule] = [finance_rules, guest_rules, ride_rules, staff_rules, scenery_rules]
