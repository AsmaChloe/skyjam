import json
import os

class JsonUtils:
    @staticmethod
    def load_json(file_path, default=None):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return default if default is not None else {}
    @staticmethod
    def save_json(file_path, data):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f)