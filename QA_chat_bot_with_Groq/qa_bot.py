import os
from dotenv import load_dotenv

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
def qa_bot(file, query):
    llm_model = llm()
    retriever_obj = retriever(file)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_model,
        chain_type="stuff",
        retriever=retriever_obj,
        return_source_documents=False
    )
    response = qa_chain.invoke(query)
    return response['result']

## Gradio interface
rag_application = gr.Interface(
    fn=qa_bot,
    inputs=[
        gr.File(label="Upload PDF file"),
        gr.Textbox(lines=2,placeholder="Enter your question here")
    ],
    outputs=gr.Textbox(label="Answer from Bot"),
    title="PDF QA bot using LLM",
    description="Upload a PDF file and ask questions about its content."
)

if __name__ == "__main__":
    rag_application.launch(
        server_name="127.0.0.1"
        , server_port=7080
    )

# if __name__ == "__main__":
#     embedding = embedding_model()
#     print(embedding.embed_query("What is the capital of France?"))