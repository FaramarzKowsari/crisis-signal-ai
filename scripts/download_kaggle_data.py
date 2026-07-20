"""Download the Kaggle NLP Getting Started competition data.

Prerequisites:
1. Accept the competition rules in the Kaggle web interface.
2. Install and configure the official Kaggle CLI.
3. Run this script from the repository root.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def main() -> None:
    if shutil.which("kaggle") is None:
        raise SystemExit("Kaggle CLI not found. Install it and configure credentials first.")
    destination = Path("data/raw/kaggle-nlp-getting-started")
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "kaggle",
            "competitions",
            "download",
            "-c",
            "nlp-getting-started",
            "-p",
            str(destination),
        ],
        check=True,
    )
    print(f"Downloaded archive to {destination}. Review the competition license before use.")


if __name__ == "__main__":
    main()
