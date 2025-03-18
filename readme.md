# RAG System with FastAPI & Groq

This project is a **Retrieval-Augmented Generation (RAG) System** built using **FastAPI** and **Groq's LLM**. It enables users to:
- Ingest **PDF documents** into a vector database (ChromaDB).
- Query the database using **natural language**.
- Retrieve relevant document chunks and metadata.
- Generate AI-powered responses using **Groq's LLM**.

---

## 📌 Features
- **FastAPI-based API** for querying documents.
- **Document ingestion system** for processing PDFs.
- **ChromaDB integration** for storing and retrieving vectorized documents.
- **Groq AI-powered responses** based on retrieved document context.
- **Metadata filtering** for refining document retrieval (class, subject, chapter).
- **Poetry for package management** to ensure a clean and isolated environment.

---

## 📦 Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/rag-system.git
cd rag-system
```

### **2. Install Poetry** (if not installed)
```bash
pip install poetry
```

### **3. Install Dependencies**
```bash
poetry install
```

### **4. Set Up Environment Variables**
Create a `.env` file and add the following variables:
```ini
GROQ_API_KEY=your_groq_api_key
VECTOR_DB_PATH=./data/vector_db
LLM_MODEL=gemma2-9b-it
```

---

## 🚀 Running the Application

### **Start the FastAPI Server**
```bash
poetry run uvicorn app.main:app --reload
```
The API will be available at: `http://127.0.0.1:8000`

---

## 📜 API Endpoints

### **1️⃣ Home Route**
- **URL:** `/`
- **Method:** `GET`
- **Description:** Returns a welcome message.
- **Example Response:**
```json
{
  "message": "Welcome to the Groq-based RAG API"
}
```

### **2️⃣ Query Documents**
- **URL:** `/query`
- **Method:** `GET`
- **Description:** Queries the vector database to retrieve relevant documents and generates a response using Groq.
- **Query Parameters:**
  - `q` (string) - The query text.
  - `class_name` (string, optional) - Filter by class (e.g., "Class 8").
  - `subject` (string, optional) - Filter by subject (e.g., "Geo").
  - `chapter` (string, optional) - Filter by chapter (e.g., "Chapter 1").
- **Example Request:**
```bash
curl -X 'GET' 'http://localhost:8000/query?q=What is global warming?&class_name=Class 8&subject=Geo'
```
- **Example Response:**
```json
{
  "query": "What is global warming?",
  "response": "Global warming refers to the long-term increase in Earth's average temperature...",
  "metadata": [{"class": "Class 8", "subject": "Geo", "chapter": "Chapter 3"}]
}
```

### **3️⃣ Ingest Documents**
- **URL:** `/ingest`
- **Method:** `POST`
- **Description:** Ingests all PDFs from the specified folder and stores them in the vector database.
- **Body Parameters:**
  - `folder_path` (string) - Path to the folder containing PDFs.
- **Example Request:**
```bash
curl -X 'POST' 'http://localhost:8000/ingest' -H 'Content-Type: application/json' -d '{"folder_path": "/path/to/pdf/folder"}'
```
- **Example Response:**
```json
{
  "message": "Documents from /path/to/pdf/folder have been successfully ingested into the vector database."
}
```

---

## 📂 Project Structure
```
rag-system/
│── app/
│   ├── main.py          # FastAPI application
│   ├── retrieval.py     # Handles document retrieval from ChromaDB
│   ├── ingestion.py     # Processes PDF documents and stores vectors
│   ├── config.py        # Configuration settings
│   ├── logger.py        # Logging setup
│── data/                # Stores the vector database
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── pyproject.toml       # Poetry dependency manager
```

---

## 🛠 Troubleshooting

### **1. Poetry Not Found?**
If you get a `command not found: poetry` error, ensure you have added Poetry to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### **2. Invalid Folder Path for Ingestion?**
Ensure the folder contains valid PDFs and is accessible.
```bash
ls /path/to/pdf/folder
```

### **3. Groq API Key Issues?**
- Ensure your **GROQ_API_KEY** is valid and correctly set in `.env`.
- If using a remote server, check network permissions.

---

## 📌 Future Improvements
- 📝 **Improve metadata handling** in retrieval.
- 🚀 **Optimize embeddings** for faster queries.
- 🤖 **Enhance AI responses** using fine-tuned models.

---

## 📜 License
This project is licensed under the **MIT License**.

🚀 **Now you're ready to use the RAG system!** 🎉

