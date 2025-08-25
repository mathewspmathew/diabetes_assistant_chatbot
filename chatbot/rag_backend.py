# rag_backend.py

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI  # <-- IMPORT GEMINI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURATION ---
FAISS_INDEX_PATH = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Load environment variables from .env file
load_dotenv()

# --- VERIFY API KEY IS AVAILABLE ---
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file. Please add it.")

def get_rag_chain():
    """
    Initializes and returns a RAG chain configured for Gemini Pro.
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found at {FAISS_INDEX_PATH}. Please run build_vectorstore.py first.")
    
    # 1. Load embedding model (no changes here)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # 2. Load the FAISS index (no changes here)
    db = FAISS.load_local(
        FAISS_INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # 3. Create a retriever (no changes here)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    # 4. Define the LLM as Gemini Pro <-- MAJOR CHANGE HERE
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY") # Pass the key explicitly
    )

    # 5. Define the prompt template (no changes here)
    template = """You are a helpful health assistant. Answer the user's question based only on the provided context.
    If the context does not contain the answer, state that you don't have enough information.
    Provide actionable suggestions if supported by the context.
    Always end your response with a disclaimer: "Note: I am an AI assistant, not a medical professional. Please consult a doctor for advice."

    Context:
    {context}

    Question:
    {input}

    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)

    # 6. Create the RAG chain (no changes here)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain

# Load the chain once when the module is imported
try:
    rag_chain = get_rag_chain()
    print("Gemini RAG chain initialized successfully.")
except (FileNotFoundError, ValueError) as e:
    rag_chain = None
    print(f"Error initializing Gemini RAG chain: {e}")

def get_rag_response(query: str):
    """
    Gets a response from the RAG chain for a given query.
    """
    if rag_chain is None:
        return "Error: The RAG system is not initialized. Please build the vector store first and check your API key."
        
    try:
        response = rag_chain.invoke({"input": query})
        return response["answer"]
    except Exception as e:
        # Catch potential API errors from Google
        return f"An error occurred while communicating with the Gemini API: {e}"