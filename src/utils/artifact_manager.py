import json
from pathlib import Path
from datetime import datetime


class ArtifactManager:

    def __init__(self):

        timestamp = datetime.utcnow().strftime(
            "%Y%m%d_%H%M%S"
        )

        self.run_dir = (
            Path("artifacts")
            / datetime.utcnow().strftime("%Y-%m-%d")
            / f"run_{timestamp}"
        )

        self.run_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ----------------------------------------
    # Save JSON
    # ----------------------------------------

    def save_json(self, filename: str, data):

        path = self.run_dir / filename

        with open(path, "w") as f:

            json.dump(
                data,
                f,
                indent=2,
                default=str
            )

    # ----------------------------------------
    # Save Text
    # ----------------------------------------

    def save_text(self, filename: str, content: str):

        path = self.run_dir / filename

        with open(path, "w") as f:
            f.write(content)

    # ----------------------------------------
    # Save Screenshot Path
    # ----------------------------------------

    def screenshot_path(self, filename="dashboard.png"):

        screenshots = self.run_dir / "screenshots"

        screenshots.mkdir(
            exist_ok=True
        )

        return screenshots / filename