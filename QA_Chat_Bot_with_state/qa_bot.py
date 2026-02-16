import os
from dotenv import load_dotenv
import chromadb

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

import gradio as gr

load_dotenv("../.env")

GROQ_API_KEY = os.getenv("GROQ")

## LLMf llm():
def llm():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile"
        , temperature=0
        , api_key=GROQ_API_KEY
    )
    return llm


## Document loader
def load_docs(file):
    loader = PyMuPDFLoader(file)
    doc = loader.load()
    return doc

## Split the documents into chunks
def split_docs(doc):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(doc)
    return chunks

## Embedding model
def embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name = "all-MiniLM-L6-v2"
    )
    return embedding_model

## Create vector store
def create_vector_store(chunks, embedding_model):
    # need to clean the chunks
    # any chunk less than 20 characters will be removed
    clean_chunks = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= 20]
    
    # need to clear the collection before adding new documents
    client = chromadb.Client()
    try:
        client.delete_collection("pdf_docs")
        print("Existing collection 'pdf_docs' deleted.")
    except Exception as e:
        pass
    
    vector_store = Chroma.from_documents(
        documents=clean_chunks,
        embedding=embedding_model,
        collection_name="pdf_docs"
    )
    
    return vector_store

## Retriever
def retriever(file):
    docs = load_docs(file)
    chunks = split_docs(docs)
    embedding = embedding_model()
    vector_store = create_vector_store(chunks, embedding)
    retriever = vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={"k":3}
    )
    return retriever

## QA bot
def qa_bot(file, query, history_state):
    # 1. Initialize state if empty
    if history_state is None:
        history_state = {"qa_chain": None, "last_file_name": None}
    
    # 2. Extract values
    qa_chain = history_state.get("qa_chain")
    last_file_name = history_state.get("last_file_name")

    # 3. Check if we need to parse or re-parse
    # Note: 'file' is a dictionary-like object in newer Gradio versions
    current_file_path = file.name if file else None

    if qa_chain is None or current_file_path != last_file_name:
        if file is None:
            return "Please upload a PDF first.", history_state
            
        print(f"Status: Parsing new document: {current_file_path}")
        llm_model = llm()
        retriever_obj = retriever(file) # Ensure this function accepts the file object
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=retriever_obj,
            return_source_documents=False
        )
        
        # Save to state
        history_state["qa_chain"] = qa_chain
        history_state["last_file_name"] = current_file_path

    # 4. Invoke the chain
    print("Status: Querying LLM...")
    response = qa_chain.invoke(query)
    
    # 5. Return the text AND the state to be saved
    return response['result'], history_state

# --- BUILD THE UI ---
with gr.Blocks() as rag_application:
    gr.Markdown("# PDF QA Bot")
    
    # Explicitly create the state component
    state_storage = gr.State(None)
    
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload PDF file")
            query_input = gr.Textbox(lines=2, label="Your Question")
            submit_btn = gr.Button("Ask Question")
        
        with gr.Column():
            output_text = gr.Textbox(label="Answer from Bot")

    # This is where we explicitly map the 3 inputs to the function
    submit_btn.click(
        fn=qa_bot,
        inputs=[file_input, query_input, state_storage],
        outputs=[output_text, state_storage]
    )

if __name__ == "__main__":
    rag_application.launch(server_name="127.0.0.1", server_port=7080)