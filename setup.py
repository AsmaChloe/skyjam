import sys
import os
from utils.JsonUtil import JsonUtil
from cx_Freeze import setup, Executable

def get_files_in_directory(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append((file_path, file_path))
    return file_paths


current_dir = os.path.dirname(os.path.abspath(__file__))
scoring_json_file_path = os.path.join(current_dir, 'save', 'scoring.json')
scoring_json_file = JsonUtil.load_json(scoring_json_file_path)
scoring_json_file["best"] = 0

JsonUtil.save_json(scoring_json_file_path, scoring_json_file)

# Dépendances
build_exe_options = {
    "packages": ["pygame"],
    "include_files": [
        *get_files_in_directory("entity"),
        *get_files_in_directory("fonts"),
        *get_files_in_directory("graphics"),
        *get_files_in_directory("img"),
        *get_files_in_directory("music"),
        *get_files_in_directory("sound"),
        *get_files_in_directory("save")
    ],
    "excludes": ["tkinter"],
    "build_exe": "pitfall_miner"
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Pitfall Miner",
    version="1.0",
    description="Un mineur qui mine et qui tombe dans le vide...",
    options={"build_exe": build_exe_options},
    executables=[Executable("pitfall_miner.py", base=base, icon="img/icon/logo")]
)


