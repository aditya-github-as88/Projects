# config.py
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# Validate all required keys exist
required_keys = ["GROQ_API_KEY"]
missing = [k for k in required_keys if not os.environ.get(k)]
if missing:
    raise EnvironmentError(f"Missing environment variables: {missing}")