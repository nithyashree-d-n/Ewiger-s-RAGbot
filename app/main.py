import os
from typing import Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from groq import Groq

# 1. Load the API Key from the .env file
# In app/main.py
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ ERROR: GROQ_API_KEY not found in .env file!")
client = Groq(api_key=api_key)


app = FastAPI()
security = HTTPBasic()

# 2. Initialize Embeddings and Vector DB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# 3. Initialize Groq using the environment variable
#client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# User Database (Ensure 'Fury' is there for C-Level testing)
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"},
    "Fury": {"password": "shield123", "role": "c-level"}
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": credentials.username, "role": user["role"]}

@app.post("/chat")
def query(message: str, user=Depends(authenticate)):
    role = user["role"].lower()
    
    # Secure Metadata Filtering
    search_filter = {"$or": [{"role": role}, {"role": "general"}]}
    if role == "c-level": search_filter = None

    # Retrieve docs
    docs = vector_db.similarity_search(message, k=3, filter=search_filter)
    
    # IMPORTANT: Handle the 'No Docs Found' case clearly before calling Groq
    if not docs:
        return {
            "answer": "I am sorry, but I do not have access to any information regarding that request based on your current permissions.",
            "sources": []
        }

    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are Ewiger, a helpful corporate assistant. Answer using ONLY this context: {context_text}"
                },
                {"role": "user", "content": message}
            ],
            # Change this line inside your chat_completion logic:
            model="llama-3.1-8b-instant",  # Updated from llama3-8b-8192,
        )
        ai_answer = completion.choices[0].message.content # Note the [0] index
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise HTTPException(status_code=500, detail="Ewiger is having trouble thinking. Check the logs.")

    sources = list(set([doc.metadata.get("role", "general") for doc in docs]))
    return {"user": user["username"], "answer": ai_answer, "sources": sources}

@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}
