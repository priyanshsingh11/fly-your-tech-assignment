# Fly Your Tech - Project Documentation

## 1. Executive Summary
The **Fly Your Tech AI Chatbot** is a modular, high-performance RAG (Retrieval-Augmented Generation) application designed to handle company-specific inquiries and lead management. It leverages state-of-the-art LLMs via Groq, a graph-based orchestration layer with LangGraph, and a local vector store for cost-effective and efficient retrieval.

---

## 2. Tech Stack Details

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Chosen for its high performance, asynchronous support, and automatic documentation (OpenAPI).
- **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) - Used to build a stateful, multi-turn agent that can reliably switch between the chatbot and its tools.
- **LLM**: **Groq (Llama-3.3-70b-versatile)** - Provides exceptionally fast inference speeds and high intelligence for complex tool-calling tasks.
- **RAG & Vector Store**: [FAISS](https://github.com/facebookresearch/faiss) - A robust library for efficient similarity search, combined with **HuggingFace (all-MiniLM-L6-v2)** for local, free embeddings.
- **Data Handling**: [LangChain](https://www.langchain.com/) - Simplifies the integration between the LLM, loaders, and vector stores.

### Frontend
- **Framework**: [React](https://reactjs.org/) (via Vite) - For a modern, responsive, and extremely fast user interface.
- **Styling**: Vanilla CSS with a focus on clean, professional design and smooth micro-interactions.
- **Communication**: [Axios](https://axios-http.com/) / Native Fetch - To interact with the FastAPI backend endpoints.

---

## 3. System Design & Architecture
flowchart LR
``` mermaid

    %% User Interaction
    User --> UI

    %% Frontend
    UI[Frontend\nReact + Vite]
        -->|HTTP Requests| API

    %% Backend / API Layer
    API[FastAPI Backend\nREST Endpoints]
        -->|State Orchestration| LG

    LG[LangGraph\nConversation State]
        -->|Prompt + Context| LLM

    %% LLM
    LLM[Groq LPU\nLlama 3.3 70B]
        -->|Model Response| LG

    %% Tools
    LG -->|Retrieve Knowledge| RAG
    LG -->|Structured Output| Leads
    LG -->|Scheduled Tasks| Scheduler

    RAG[FAISS RAG\nCompany Data]
        --> LG

    Leads[Leads Engine\nJSON Parsing]
        --> LG

    Scheduler[Scheduler\nMock API]
        --> LG

    %% Response Flow Back
    LG --> API
    API --> UI
    UI --> User
```

### RAG (Retrieval-Augmented Generation) Workflow
1.  **Ingestion**: The system reads `company_data.txt` using LangChain's `TextLoader`.
2.  **Chunking**: Data is split into manageable chunks (500 characters with 50-character overlap) for precise retrieval.
3.  **Embedding**: Chunks are converted into vector representations using a local HuggingFace model.
4.  **Retrieval**: When a query hits the `company_info_tool`, FAISS searches for the most relevant context and hands it to the LLM.

### Agentic Flow (LangGraph)
The chatbot operates as a directed acyclic graph (DAG):
- **START**: Receives the user message and initializes the conversation state.
- **Chatbot Node**: Evaluates the message. It can:
    - Respond directly (e.g., greetings, general questions).
    - Call a tool (e.g., if asked about company services or leads).
    - Terminate (if specific exit words like "bye" are detected).
- **Tools Node**: Executes the specified tool (FAISS search, JSON lead lookup, or dummy scheduling) and feeds the output back to the chatbot for summarization.
- **END**: Returns the final response to the user.

---

## 4. Implementation Logic

### Key Components

#### 1. `tools.py`
- `company_info_tool`: Interacts with the FAISS retriever.
- `get_all_leads`: Parses `leads.json` to provide a summary of potential clients.
- `get_lead_details`: Performs fuzzy matching to find information on a specific lead.
- `schedule_meeting`: A mock tool demonstrating how the agent could interact with external APIs (e.g., Cal.com, Google Calendar).

#### 2. `graph.py`
- Defines the `State` using `TypedDict` and `Annotated` to manage message history.
- Binds the LLM with the defined tools.
- Implements the routing logic (conditional edges) between the LLM and the tools.

#### 3. `main.py`
- Sets up the FastAPI server with CORS enabled for frontend integration.
- Exposes a `/chat` POST endpoint that invokes the LangGraph instance.

---

## 5. Planning & Approach

### Design Philosophy
- **Modularity**: Every component (Tools, RAG, API, Graph) is isolated, allowing for easy updates or replacement of the LLM/Vector store.
- **Cost Efficiency**: By using local embeddings (`HuggingFaceEmbeddings`) and the free tier of Groq, the entire system is highly capable while remaining cost-effective for development.
- **Performance**: Groq's LPU (Language Processing Unit) inference coupled with FastAPI ensures sub-second response times for a "fluid" chat experience.

### Security & Lead Management
- Leads are handled as structured JSON data, allowing the LLM to format them into professional tables or lists rather than raw data dumps, ensuring a polished user experience.

---

## 6. Setup & Execution Summary
- **Backend**: Python environment with `uvicorn` serving the FastAPI app on port 8000.
- **Frontend**: Vite development server running on port 5173.
- **Deployment Ready**: The architecture is container-ready, with environment variables managing sensitive API keys.
