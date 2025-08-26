# Health Intelligence Hub: An AI-Powered Health Chatbot 🩺

<img width="1651" height="779" alt="image" src="https://github.com/user-attachments/assets/84c559dd-bf53-407f-871f-a91772584733" />


A Retrieval-Augmented Generation (RAG) based chatbot designed to answer diabetes relates questions by grounding its responses in a curated medical knowledge base.

---

## 🌟 Project Overview

This project addresses the critical "trust gap" in AI for sensitive domains like healthcare. General-purpose Large Language Models (LLMs) can "hallucinate" or provide outdated information, which can be dangerous.

Project solves this by using a **RAG pipeline**. Instead of answering from its general memory, the AI is given an "open-book exam" for every question. It first **retrieves** relevant information from a trusted, hand-picked set of medical documents and then **generates** an answer based *only* on that verified context.

### ✨ Core Features

-   **Conversational Q&A:** Ask questions in natural language about symptoms, diets, and health conditions.
-   **Grounded in Trusted Sources:** All answers are based on the provided documents in the `knowledge_base` directory.
-   **Reduces Hallucinations:** The RAG approach minimizes the risk of the AI inventing facts.
-   **Safe and Reliable:** Includes guardrails to prevent answering out-of-domain questions and provides a disclaimer for users.
-   **Interactive UI:** Built with Streamlit for a clean, user-friendly chat interface.

---

## 🎬 Demo

[Add a GIF or Screenshot Here]

*A brief demonstration of the chatbot answering a user's question about heart-healthy diets.*

---

## 🛠️ System Architecture

The application operates in two distinct phases:

**1. Offline: Indexing Pipeline (Building the Knowledge Base)**
This one-time process prepares the knowledge for fast retrieval.

-   **Load:** Medical documents are loaded from the `knowledge_base` folder.
-   **Chunk:** Documents are split into smaller, manageable chunks.
-   **Embed:** Each chunk is converted into a numerical vector using a `sentence-transformers` model.
-   **Store:** These vectors are stored in a highly efficient **FAISS** vector index, creating a searchable "library" of knowledge.

**2. Online: Inference Pipeline (Live Chat)**
This happens in real-time when a user interacts with the app.

-   **Query:** The user asks a question through the Streamlit UI.
-   **Retrieve:** The user's query is embedded, and FAISS is used to find the most relevant text chunks from the vector index.
-   **Augment:** The retrieved chunks (context) are combined with the original query into a detailed prompt.
-   **Generate:** The complete prompt is sent to the **Google Gemini API**, which generates a coherent, context-aware answer.

<img width="1038" height="517" alt="image" src="https://github.com/user-attachments/assets/10b77521-1bf0-4031-b2bd-8ac8d0e99b69" />


---

## 🚀 Tech Stack

-   **Frontend:** Streamlit
-   **AI Orchestration:** LangChain
-   **LLM:** Google Gemini Pro
-   **Vector Database:** FAISS (Facebook AI Similarity Search)
-   **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
-   **Backend:** Python
-   **Environment Management:** `python-dotenv`

---

## ⚙️ Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.9+
-   Git

Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.


### 1. Clone the Repository

```bash
git clone https://github.com/[Your-GitHub-Username]/health_rag_app.git
cd health_rag_app
