
import time
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Define paths
KNOWLEDGE_BASE_DIR = "knowledge_base"
FAISS_INDEX_PATH = "faiss_index"

def build_vector_store():
    """
    Builds and saves a FAISS vector store from documents in the knowledge base.
    """
    print("Loading documents from knowledge base...")
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.txt")
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found in the knowledge base directory.")
    
    print(f"Loaded {len(documents)} document(s).")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    print("Initializing embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Building FAISS vector store... This might take a moment.")
    start_time = time.time()
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(FAISS_INDEX_PATH)
    end_time = time.time()

    print(f"Vector store built successfully and saved to '{FAISS_INDEX_PATH}'.")
    print(f"Time taken: {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    build_vector_store()