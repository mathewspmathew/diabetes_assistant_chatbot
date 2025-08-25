# pages/1_💬_Health_Chat.py

import streamlit as st
# STEP 1: Import the REAL function and the chain object from your backend file.
from rag_backend import get_rag_response, rag_chain 

st.set_page_config(page_title="Health Chat", page_icon="💬")
st.title("💬 Health Chat")

# STEP 2: Add a check to ensure the backend loaded correctly.
# This tells the user if they forgot to build the vector store or set up the API key.
if rag_chain is None:
    st.error("RAG system is not initialized. Please ensure 'faiss_index' exists and your API key is correct. Run 'build_vectorstore.py' if needed.")
    st.stop()

st.info("Ask me about symptoms, lifestyle changes, or questions about diabetes and heart disease.")

# Initialize chat history (no changes here)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun (no changes here)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input (no changes here, but now it calls the REAL function)
if prompt := st.chat_input("What are the symptoms of diabetes?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base and thinking..."):
            # STEP 3: This now calls the powerful function from rag_backend.py
            response = get_rag_response(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})