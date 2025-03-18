import chromadb
from sentence_transformers import SentenceTransformer
from app.config import config
from app.logger import logger

class QueryRetrieval:
    def __init__(self):
        logger.info("Initializing QueryRetrieval...")
        self.client = chromadb.PersistentClient(path=config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("QueryRetrieval initialized successfully.")
        logger.info(f"Total stored documents: {self.collection.count()}")
    
    def retrieve(self, query, class_name=None, subject=None, chapter=None, top_k=5):
        logger.info(f"Processing query: '{query}'")

        # Generate embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        logger.debug(f"Generated query embedding: {query_embedding[:5]}... (truncated)")

        # Construct filters
        filter_conditions = []
        if class_name:
            filter_conditions.append({"class": {"$eq": class_name}})
        if subject:
            filter_conditions.append({"subject": {"$eq": subject}})
        if chapter:
            filter_conditions.append({"chapter": {"$eq": chapter}})
        
        where_clause = {"$and": filter_conditions} if filter_conditions else None
        logger.debug(f"Constructed filter conditions: {where_clause}")

        # Perform retrieval
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause
        )

        # Extract retrieved documents & metadata
        retrieved_docs = results.get("documents", [[]])[0]  # List of retrieved document texts
        retrieved_metadata = results.get("metadatas", [[]])[0]  # List of retrieved metadata dictionaries

        logger.info(f"Retrieved {len(retrieved_docs)} documents.")
        
        # Log metadata for debugging
        for i, meta in enumerate(retrieved_metadata):
            logger.debug(f"Metadata {i+1}: {meta}")

        return retrieved_docs, retrieved_metadata

# Example usage
retriever = QueryRetrieval()

