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

<div align="center">
  <svg width="800" height="500" viewBox="0 0 800 500" fill="none" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect width="800" height="500" rx="15" fill="#f8f9fa"/>
    <rect x="10" y="10" width="780" height="480" rx="10" stroke="#dee2e6" stroke-width="2" stroke-dasharray="5 5"/>

    <!-- Legend -->
    <rect x="630" y="30" width="140" height="80" rx="5" fill="white" stroke="#ced4da"/>
    <text x="640" y="50" font-family="Arial" font-size="12" font-weight="bold" fill="#495057">Legend</text>
    <rect x="640" y="65" width="10" height="10" fill="#007bff" rx="2"/>
    <text x="655" y="74" font-family="Arial" font-size="11" fill="#495057">UI / Interaction</text>
    <rect x="640" y="85" width="10" height="10" fill="#28a745" rx="2"/>
    <text x="655" y="94" font-family="Arial" font-size="11" fill="#495057">Processing/Logics</text>

    <!-- Frontend -->
    <rect x="50" y="200" width="140" height="80" rx="8" fill="#e7f1ff" stroke="#007bff" stroke-width="2"/>
    <text x="120" y="240" font-family="Arial" font-size="16" font-weight="bold" fill="#0056b3" text-anchor="middle">Frontend</text>
    <text x="120" y="260" font-family="Arial" font-size="12" fill="#0056b3" text-anchor="middle">(React + Vite)</text>

    <!-- API Layer -->
    <rect x="250" y="180" width="160" height="120" rx="8" fill="#f0fff4" stroke="#28a745" stroke-width="2"/>
    <text x="330" y="215" font-family="Arial" font-size="16" font-weight="bold" fill="#218838" text-anchor="middle">FastAPI</text>
    <text x="330" y="235" font-family="Arial" font-size="12" fill="#218838" text-anchor="middle">REST Endpoints</text>
    <line x1="260" y1="250" x2="400" y2="250" stroke="#28a745" stroke-width="1" stroke-dasharray="2 2"/>
    <text x="330" y="275" font-family="Arial" font-size="14" font-weight="bold" fill="#218838" text-anchor="middle">LangGraph</text>
    <text x="330" y="290" font-family="Arial" font-size="11" fill="#218838" text-anchor="middle">State Management</text>

    <!-- Brain / LLM -->
    <circle cx="550" cy="120" r="60" fill="#fff5f5" stroke="#dc3545" stroke-width="2"/>
    <text x="550" y="115" font-family="Arial" font-size="16" font-weight="bold" fill="#c82333" text-anchor="middle">Groq LPU</text>
    <text x="550" y="135" font-family="Arial" font-size="12" fill="#c82333" text-anchor="middle">Llama 3.3 70B</text>

    <!-- Data / Tools -->
    <rect x="500" y="280" width="220" height="180" rx="8" fill="#fff9db" stroke="#f1c40f" stroke-width="2"/>
    <text x="610" y="305" font-family="Arial" font-size="16" font-weight="bold" fill="#856404" text-anchor="middle">Tools & Data</text>
    
    <!-- Sub-Tools -->
    <rect x="515" y="325" width="190" height="40" rx="4" fill="white" stroke="#ffe066"/>
    <text x="610" y="350" font-family="Arial" font-size="11" fill="#856404" text-anchor="middle">FAISS RAG (Company Data)</text>
    
    <rect x="515" y="375" width="190" height="40" rx="4" fill="white" stroke="#ffe066"/>
    <text x="610" y="400" font-family="Arial" font-size="11" fill="#856404" text-anchor="middle">Leads Engine (JSON Parsing)</text>
    
    <rect x="515" y="425" width="190" height="40" rx="4" fill="white" stroke="#ffe066"/>
    <text x="610" y="450" font-family="Arial" font-size="11" fill="#856404" text-anchor="middle">Scheduler (Mock API)</text>

    <!-- Arrows -->
    <!-- Frontend <-> API -->
    <path d="M 190 240 L 240 240" stroke="#007bff" stroke-width="2" marker-end="url(#arrowhead)"/>
    <path d="M 240 260 L 190 260" stroke="#28a745" stroke-width="2" marker-end="url(#arrowhead)"/>

    <!-- API <-> LLM -->
    <path d="M 410 210 Q 480 200 500 160" stroke="#28a745" stroke-width="2" marker-end="url(#arrowhead)" fill="none"/>
    <path d="M 500 120 Q 450 140 410 180" stroke="#dc3545" stroke-width="2" marker-end="url(#arrowhead)" fill="none"/>

    <!-- API <-> Tools -->
    <path d="M 330 300 Q 330 380 490 380" stroke="#28a745" stroke-width="2" marker-end="url(#arrowhead)" fill="none"/>
    <path d="M 490 420 Q 380 420 380 300" stroke="#f1c40f" stroke-width="2" marker-end="url(#arrowhead)" fill="none"/>

    <!-- Arrowhead Definition -->
    <defs>
      <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="context-fill" />
      </marker>
    </defs>
  </svg>
</div>

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
