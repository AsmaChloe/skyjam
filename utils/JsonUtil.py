import json
import os 

class JsonUtil:
    @staticmethod
    def load_json(file_path, default=None):
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return default if default is not None else {}
    
    @staticmethod
    def save_json(file_path, data):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Données sauvegardées dans {file_path}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données : {e}")
