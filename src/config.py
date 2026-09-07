import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Read the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Check whether the key exists
if not OPENAI_API_KEY:

    raise ValueError(
        "OPENAI_API_KEY is not configured. "
        "Please add it to the .env file."
    )


print("LLM configuration loaded successfully.")