import os
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

import module.config as config

load_dotenv("../.env")

GROQ_API_KEY = os.getenv("GROQ")

def embedding_model():
    embed_model = HuggingFaceEmbedding(
        model_name=config.EMBDEDDING_MODEL_NAME
    )

def llm():
    llm = Groq(
        model=config.LLM_NAME,
        temperature=0,
        api_key=GROQ_API_KEY
    )
    return llm