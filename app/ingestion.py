import os
import re
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from sentence_transformers import SentenceTransformer
from app.config import config
from app.logger import logger

class DocumentIngestion:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.client = chromadb.PersistentClient(path=config.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Small and efficient

    def extract_text(self, pdf_path):
        logger.info(f"Extracting text from: {pdf_path}")
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text

    def parse_filename(self, filename):
        """Extract class, subject, and chapter from filename."""
        pattern = r"class(\d+)_([a-zA-Z]+)_c(\d+)\.pdf"
        match = re.match(pattern, filename)
        if match:
            class_num, subject, chapter_num = match.groups()
            return f"Class {class_num}", subject.capitalize(), f"Chapter {chapter_num}"
        else:
            logger.warning(f"Filename {filename} does not match expected format.")
            return None, None, None

    def process_documents(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".pdf"):
                class_name, subject, chapter = self.parse_filename(filename)
                if not class_name or not subject or not chapter:
                    continue  # Skip files with incorrect naming

                pdf_path = os.path.join(self.data_dir, filename)
                text = self.extract_text(pdf_path)

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
                chunks = text_splitter.split_text(text)

                for idx, chunk in enumerate(chunks):
                    embedding = self.embedding_model.encode(chunk).tolist()
                    doc_id = f"{filename}-{idx}"

                    self.collection.add(
                        ids=[doc_id],
                        documents=[chunk],  # ✅ Add the actual text content here
                        embeddings=[embedding],
                        metadatas=[
                            {"class": class_name, "subject": subject, "chapter": chapter, "filename": filename}
                        ]
                    )
                    logger.debug(f"Stored chunk {idx} from {filename} - {class_name}, {subject}, {chapter}")

if __name__ == "__main__":
    ingest = DocumentIngestion()
    ingest.process_documents()
    logger.info("Document ingestion completed.")
