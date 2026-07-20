"""Synthetic examples for local smoke tests and demonstrations."""

from __future__ import annotations

import csv
from pathlib import Path

ROWS = [
    ("1", "Earthquake damaged several buildings and people need rescue", 1),
    ("2", "Flash flood has blocked the main road to the hospital", 1),
    ("3", "Wildfire smoke is spreading and residents are evacuating", 1),
    ("4", "Bridge collapsed after heavy rain; emergency crews requested", 1),
    ("5", "Power lines are down across the district after the storm", 1),
    ("6", "Two people are trapped under debris near the station", 1),
    ("7", "The concert last night was absolutely fire", 0),
    ("8", "My inbox is flooded with discount emails", 0),
    ("9", "This new game is a total disaster but I still love it", 0),
    ("10", "The team destroyed its opponent in the final", 0),
    ("11", "I am burning through my reading list this weekend", 0),
    ("12", "Traffic is terrible as usual, nothing unusual happened", 0),
    ("13", "Aftershock reported; checking damaged homes now", 1),
    ("14", "Emergency shelter needs water and blankets", 1),
    ("15", "The movie plot crashed and burned halfway through", 0),
    ("16", "Storm surge entered houses along the coast", 1),
    ("17", "My phone battery is dying, send help", 0),
    ("18", "Hospital generator failed during the blackout", 1),
    ("19", "The presentation was an explosion of great ideas", 0),
    ("20", "Landslide has isolated three villages", 1),
]


def write_demo_data(output: str | Path) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["id", "text", "target"])
        writer.writerows(ROWS)
