from .data_loading import load_data
from .data_processing import split_documents, create_index
from .model import llm, embedding_model
from .config import SIMILARITY_TOP_K

from llama_index.core import Settings

Settings.llm = llm()
Settings.embed_model = embedding_model()

def rag_app(file_path, query, history_state):
    # old state coming frome the UI
    query_engine = history_state.get("query_engine")
    old_file = history_state.get("old_file")

    if query_engine is None or file_path != old_file:
        documents = load_data(file_path)
        nodes = split_documents(documents)
        index = create_index(nodes)

        query_engine = index.as_query_engine(
            similarity_top_k = SIMILARITY_TOP_K
        )
        history_state["query_engine"] = query_engine
        history_state["old_file"] = file_path
    else:
        print("Using cached query engine")

    response = query_engine.query(
        query
    )

    return str(response), history_state