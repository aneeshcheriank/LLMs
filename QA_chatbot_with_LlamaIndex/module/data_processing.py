from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings

import module.config as config
import module.model as model
from module.vector_store import create_storage_context


Settings.embed_model = model.embedding_model()


def split_documents(documents):
    parser = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE, 
        chunk_overlap=config.CHUNK_OVERLAP
    )

    nodes = parser.get_nodes_from_documents(
        documents,
        show_progress=False
    )
    return nodes

def create_index(nodes):
    index = VectorStoreIndex(
        nodes = nodes,
        storage_context= create_storage_context()
        , embed_model=Settings.embed_model
    )
    return index