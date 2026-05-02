# Ewiger: Enterprise RAG Chatbot with RBAC

**Ewiger** is a secure, production-ready internal chatbot designed to handle sensitive company data. Built on a **Retrieval-Augmented Generation (RAG)** architecture, it allows employees to query internal documentation while strictly enforcing **Role-Based Access Control (RBAC)**.

Unlike standard chatbots, Ewiger "thinks" before it speaks. It verifies the user's identity and department (HR, Finance, Engineering, etc.) and uses **metadata filtering** to ensure that confidential information never leaks to unauthorized users.

### 🌟 Key Features
- **Security-First RAG**: Implements metadata-level filtering within the vector database to restrict data retrieval based on user roles.
- **Role-Based Access Control (RBAC)**: Supports multiple roles (Engineering, Finance, HR, Marketing, and C-Level) with unique permission sets.
- **Intelligent Responses**: Powered by **Llama 3.1 (via Groq)** for lightning-fast, conversational, and context-aware answers.
- **Source Transparency**: Every answer includes citations to the specific internal documents used as context.
- **Zero-Hallucination Guardrails**: Strict system prompting ensures the assistant only answers based on provided company data.

### 🛠️ The Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **LLM**: Llama 3.1 (8B/70B) via Groq Cloud API
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2`
- **Environment Management**: Python-Dotenv for secure API key handling


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
