# Fly Your Tech AI Chatbot

A simple, clean, and modular AI-powered chatbot implementation for the "Fly Your Tech" assignment.

## Tech Stack
- **Backend**: Python (FastAPI, LangChain, LangGraph, FAISS)
- **LLM**: Groq (Llama-3.3-70b-versatile)
- **Embeddings**: HuggingFace (Local - `all-MiniLM-L6-v2`)
- **Frontend**: React (Vite)

## Architecture Overview

### 1. RAG Flow (Knowledge Base)
- **Source**: `company_data.txt` contains dummy info about "Fly Your Tech".
- **Process**: LangChain loads the text, splits it into chunks.
- **Embeddings**: Uses **HuggingFace (local)** embeddings to create the vector store. This is free and doesn't require an API key.
- **Retrieval**: When a user asks about the company, the `company_info_tool` uses a FAISS vector store to retrieve relevant context.

### 2. Tool Calling Logic
- The LLM (**Llama 3.3 via Groq**) is "bound" with three tools:
  - `company_info_tool`: For company-related questions (Address, Services, etc.).
  - `get_all_leads`: For retrieving data from `leads.json`.
  - `schedule_meeting`: A dummy tool for scheduling requests.
- Based on the user's intent, the LLM decides which tool to call or if it can answer directly.

### 3. LangGraph Flow
- A `StateGraph` manages the conversation state.
- **START** → **chatbot** (LLM decides)
- **chatbot** → **tools** (if a tool is needed) → **chatbot** (to summarize tool output)
- **chatbot** → **END** (if a final answer is ready)

## How to Run

### 1. Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create a `.env` file and add your Google API Key:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: I've installed them in the venv during the automated setup)*
4. Run the server:
   ```bash
   python main.py
   ```

### 2. Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Dummy Data Used
- `company_data.txt`: Contains mission, address, email, and service list.
- `leads.json`: Contains a small list of dummy prospective clients.
