import dotenv
import os

# 1. Load the environment variables immediately.
# We manually resolve the path here to guarantee it loads before any local imports run.
# This assumes your .env file is in the root directory of the project.
dotenv.load_dotenv(dotenv.find_dotenv())

def config_env():
    API_KEY = os.getenv("GROQ")
    if API_KEY is None:
        raise ValueError("GROQ API key not found in environment variables.")
    os.environ["GROQ_API_KEY"] = API_KEY