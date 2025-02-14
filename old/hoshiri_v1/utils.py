import os
import json
from config import DATABASE_PATH


def ensure_data_directory():
    """Ensure the data directory and metadata file exist."""
    data_dir = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(DATABASE_PATH):
        with open(DATABASE_PATH, "w") as f:
            json.dump({}, f, indent=4)


def load_metadata():
    ensure_data_directory()
    with open(DATABASE_PATH, "r") as f:
        return json.load(f)


def save_metadata(data):
    ensure_data_directory()
    with open(DATABASE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_available_scripts():
    return [f.replace(".py", "") for f in os.listdir("modules") if f.endswith(".py")]
