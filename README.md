# DS RPC 01: Ewiger - Internal RAG Chatbot with RBAC

This is the completed solution for the [Resume Project Challenge](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge). **Ewiger** is an AI-powered internal chatbot that uses Retrieval-Augmented Generation (RAG) and Role-Based Access Control (RBAC) to ensure users only see data they are authorized to access.

![alt text](resources/RPC_01_Thumbnail.jpg)

### 🔐 Roles & Permissions
- **engineering**: Technical docs & general info.
- **finance**: Financial reports & general info.
- **hr**: Employee records & general info.
- **marketing**: Campaign metrics & general info.
- **c-level**: Full access to all departments.
- **general**: Basic company policies and FAQs only.

---

## 🚀 How to Run the Project

### 1. Prerequisites
Ensure your virtual environment is active and you have created a `.env` file in the root directory:
```text
GROQ_API_KEY=your_groq_api_key_here
```

### 2. Ingest Data
Before running the app for the first time, populate the vector database:
```bash
../venv/bin/python3 ingest.py
```

### 3. Start the Backend (Terminal 1)
Run the FastAPI server with RBAC logic:
```bash
../venv/bin/python3 -m uvicorn app.main:app --reload
```

### 4. Start the Frontend (Terminal 2)
Launch the Streamlit chat interface:
```bash
../venv/bin/python3 -m streamlit run streamlit_app.py
```

---

## 🛠️ Tech Stack
- **Framework**: FastAPI (Backend) & Streamlit (UI)
- **Vector DB**: ChromaDB
- **LLM**: Llama 3 (via Groq API)
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **Security**: HTTPBasic Auth with Metadata Filtering
