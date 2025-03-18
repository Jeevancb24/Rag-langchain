import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    LLM_MODEL = os.getenv('LLM_MODEL')  # Groq model
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH')

config = Config()
