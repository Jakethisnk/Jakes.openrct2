# Jakes.openrct2

A rule-based park management assistant for [OpenRCT2](https://openrct2.io). It analyzes park
state (finances, guests, rides, staff, scenery) and prints prioritized recommendations.

## Usage

Requires Python 3.10+. No dependencies.

```
python -m assistant                       # analyze the struggling mock park
python -m assistant --mock healthy_park   # analyze the healthy mock park
python -m assistant --file my_park.json   # analyze your own park-state JSON
python -m unittest discover -s tests      # run tests
```

## Layout

- `assistant/state/` – `ParkState` data model and loaders (JSON / mock)
- `assistant/logic/` – recommendation types and rules
- `assistant/engine/` – `Assistant` that runs rules and sorts by priority
- `assistant/data/` – mock park data (see it for the JSON schema)
- `assistant/cli.py` – command-line interface

## Current capabilities

Advice on cash/loan/income, guest happiness and needs, ride maintenance and queues,
staff adequacy (handymen, mechanics, entertainers, security), and litter/scenery/vandalism.

## Extending

Add a rule function to `ALL_RULES` in `assistant/logic/rules.py`, or implement a new
loader in `assistant/state/loader.py` (a class with `load() -> ParkState`) to read real
OpenRCT2 save files or plugin exports.
