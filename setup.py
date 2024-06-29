import sys
import os
from cx_Freeze import setup, Executable

def get_files_in_directory(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append((file_path, file_path))
    return file_paths

# Dépendances
build_exe_options = {
    "packages": ["pygame"],
    "include_files": [
        *get_files_in_directory("entity"),
        *get_files_in_directory("fonts"),
        *get_files_in_directory("graphics"),
        *get_files_in_directory("img"),
        *get_files_in_directory("music"),
        *get_files_in_directory("util"),
        *get_files_in_directory("sound")
    ],
    "excludes": ["tkinter"],
    "build_exe": "skyjam_apericube"
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Un jeu sans nom pour le moment",
    version="0.1",
    description="Le jeu des apéricubes pour la Skyjam",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)


