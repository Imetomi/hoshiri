import os
import subprocess
from config import MODULES_DIR
from utils import load_metadata, save_metadata


def generate_script(name, code):
    script_name = name.replace(" ", "_").lower()
    script_path = os.path.join(MODULES_DIR, f"{script_name}.py")

    with open(script_path, "w") as f:
        f.write(code)

    metadata = load_metadata()
    metadata[script_name] = {"path": script_path}
    save_metadata(metadata)

    return script_name


def execute_script(name):
    script_path = os.path.join(MODULES_DIR, f"{name}.py")

    if not os.path.exists(script_path):
        print(f"Error: Script '{name}' not found.")
        return

    subprocess.run(["python", script_path])
