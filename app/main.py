import os
from fastapi import FastAPI, Query, UploadFile, File
from langchain_groq import ChatGroq
from app.retrieval import retriever
from app.ingestion import DocumentIngestion
from app.logger import logger
from app.config import config

app = FastAPI(title="RAG System with Groq", version="1.0")
llm = ChatGroq(groq_api_key=config.GROQ_API_KEY, model=config.LLM_MODEL)
ingestor = DocumentIngestion()  # Instantiate the ingestion class


@app.get("/")
def home():
    return {"message": "Welcome to the Groq-based RAG API"}


@app.get("/query")
def query_docs(
    q: str, 
    class_name: str = Query(None, description="Filter by class (e.g., 'Class 8')"),
    subject: str = Query(None, description="Filter by subject (e.g., 'Geo')"),
    chapter: str = Query(None, description="Filter by chapter (e.g., 'Chapter 1')")
):
    logger.info(f"Received query: '{q}' with filters - Class: {class_name}, Subject: {subject}, Chapter: {chapter}")

    # Retrieve relevant chunks and metadata
    retrieved_docs, retrieved_metadata = retriever.retrieve(q, class_name=class_name, subject=subject, chapter=chapter)

    if not retrieved_docs:
        return {"query": q, "response": "No relevant documents found.", "metadata": []}

    # Flatten lists if needed
    if isinstance(retrieved_docs[0], list):
        retrieved_docs = [item for sublist in retrieved_docs for item in sublist]
    
    if isinstance(retrieved_metadata[0], list):
        retrieved_metadata = [item for sublist in retrieved_metadata for item in sublist]

    context = "\n".join(filter(None, retrieved_docs))

    # Generate response using Groq
    prompt = f"""DOCUMENT: {context}
                USER_QUESTION: {q}
                INSTRUCTIONS:
                Answer the user's QUESTION using the DOCUMENT text above.
                Keep your answer grounded in the facts of the DOCUMENT.
                If the DOCUMENT doesn’t contain the facts to answer the USER_QUESTION, return:
                'Provided context doesn't really contain the answer to the question.'"""

    response = llm.invoke(prompt)

    return {
        "query": q,
        "response": response.content,
        "metadata": retrieved_metadata
    }


@app.post("/ingest")
def ingest_documents(folder_path: str):
    """
    Endpoint to ingest PDF documents from a given folder path.
    """
    logger.info(f"Received request to ingest PDFs from folder: {folder_path}")

    # Check if the folder exists
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        logger.error(f"Invalid folder path: {folder_path}")
        return {"error": "Invalid folder path. Please provide a valid directory containing PDFs."}

    # Set the ingestion class to use the provided folder
    ingestor.data_dir = folder_path

    # Process documents
    ingestor.process_documents()

    return {"message": f"Documents from {folder_path} have been successfully ingested into the vector database."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
