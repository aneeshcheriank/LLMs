"""
configure the model for agents
"""

import dotenv
import os
from langchain_groq import ChatGroq

from src.configuration import DOTENV_PATH, MODEL

try:
    dotenv.load_dotenv(DOTENV_PATH)
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ")
except FileNotFoundErrorError:
    print(f"file: {DOTENV_PATH} not found")


def llm():
    llm = ChatGroq(
        model=MODEL,
        provider='groq',
        temperature=0.0
    )

    return llm