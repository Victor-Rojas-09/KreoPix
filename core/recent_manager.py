import json
import os


class RecentManager:
    """Manages recently opened projects."""

    def __init__(self, max_items=10):
        self.max_items = max_items
        self.file_path = "data/recent_projects.json"
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def get_recent(self):
        with open(self.file_path, "r") as f:
            return json.load(f)

    def add_recent(self, path):
        recent = self.get_recent()

        if path in recent:
            recent.remove(path)

        recent.insert(0, path)
        recent = recent[:self.max_items]

        with open(self.file_path, "w") as f:
            json.dump(recent, f)