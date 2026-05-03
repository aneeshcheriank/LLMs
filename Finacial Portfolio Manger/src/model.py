"""
configure the model for agents
"""

# Now that the environment is loaded, it's safe to import your configuration
from src.configuration import MODEL
from src.environment import config_env

# 4. Import LangChain now that the API key is securely set in os.environ
from langchain_groq import ChatGroq

def get_llm():
    config_env()

    return ChatGroq(
        model=MODEL,
        temperature=0.0
    )