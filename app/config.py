import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Local scheme database path
DATA_PATH = BASE_DIR / "app" / "data" / "schemes_data.json"
