import json
import pathlib


class DataStorage:
    def __init__(self, file_path="storage/data.json"):
        self.file_path = pathlib.Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def read_data(self):
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def write_data(self, data):
        existing_data = self.read_data()
        existing_data.update(data)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
