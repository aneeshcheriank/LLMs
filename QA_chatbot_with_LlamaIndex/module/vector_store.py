import chromadb
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

def create_storage_context():
    db = chromadb.PersistentClient(path="./chroma_db")
    
    # if collection exists, delete it
    try:
        db.delete_collection("qa_bot_collection")
        print("Existing collection 'qa_bot_collection' deleted.")
    except Exception as e:
        pass

    chroma_collection = db.create_collection(
        name="qa_bot_collection"
    )
    vector_store = ChromaVectorStore(
        chroma_collection=chroma_collection
    )
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )
    return storage_context
