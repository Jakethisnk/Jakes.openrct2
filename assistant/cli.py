from __future__ import annotations

import argparse
import sys

from .engine import Assistant
from .state.loader import JsonFileSource, MockSource


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="OpenRCT2 park assistant")
    ap.add_argument("--mock", default="struggling_park",
                    help="mock park name (struggling_park or healthy_park)")
    ap.add_argument("--file", help="path to a park state JSON file")
    args = ap.parse_args(argv)

    try:
        source = JsonFileSource(args.file) if args.file else MockSource(args.mock)
        park = source.load()
    except (OSError, ValueError, TypeError) as e:
        print(f"Error loading park data: {e}", file=sys.stderr)
        return 1

    recs = Assistant().analyze(park)
    print(f"=== {park.name} ===")
    if not recs:
        print("Everything looks good!")
    for r in recs:
        print(f"[{r.priority.name:<6}] ({r.category}) {r.message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
