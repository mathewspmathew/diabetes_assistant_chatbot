# app.py

import streamlit as st

st.set_page_config(
    page_title="Health Intelligence Hub",
    page_icon="🩺",
    layout="wide"
)

st.title("Welcome to the Health Intelligence Hub 🩺")

st.sidebar.success("Select a feature above.")

st.markdown(
    """
    This is an interactive AI application for health insights.
    
    ### How to Use
    
    1.  **Select 'Health Chat' from the sidebar** to start asking questions.
    2.  You can ask about symptoms, diet, exercise, and conditions covered in our knowledge base (currently Diabetes and Heart Health).
    
    **Example Questions:**
    - "What are the symptoms of type 2 diabetes?"
    - "What kind of diet is good for my heart?"
    - "Why should I reduce salt?"
    
    ---
    
    **Disclaimer:** This tool is for informational purposes only. It is not a substitute for professional medical advice. Always consult with a qualified healthcare provider.
    ### Our Commitment to Trustworthy Information

    Welcome! This AI assistant is powered by a knowledge base created from publicly available information from the world's leading health organizations. We believe in transparency, and our sources include:

    *   **World Health Organization (WHO)** - [who.int](https://www.who.int)
    *   **U.S. Centers for Disease Control and Prevention (CDC)** - [cdc.gov](https://www.cdc.gov)
    *   **UK National Health Service (NHS)** - [nhs.uk](https://www.nhs.uk)
    *   **National Library of Medicine (PubMed Central & MedlinePlus)** - [nih.gov](https://www.nih.gov)

    """
)