import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AI Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Storage
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/scripts_metadata.json")
MODULES_DIR = os.getenv("MODULES_DIR", "modules/")
