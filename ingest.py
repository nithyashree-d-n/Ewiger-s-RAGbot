import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Update path to point to where the folders actually are
DATA_PATH = "resources/data/"
CHROMA_PATH = "chroma_db"

# Initialize Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_docs():
    documents = []
    
    # Iterate through engineering, finance, general, hr, marketing
    for role in os.listdir(DATA_PATH):
        role_path = os.path.join(DATA_PATH, role)
        
        if os.path.isdir(role_path):
            print(f"Processing role: {role}")
            # Use TextLoader for .md files
            loader = DirectoryLoader(role_path, glob="*.md", loader_cls=TextLoader)
            role_docs = loader.load()
            
            # Tag every chunk with the role from the folder name
            for doc in role_docs:
                doc.metadata["role"] = role
            
            documents.extend(role_docs)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    chunks = text_splitter.split_documents(documents)

    # Create and save the Vector DB
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Success! Ingested {len(chunks)} chunks into {CHROMA_PATH}")

if __name__ == "__main__":
    ingest_docs()
