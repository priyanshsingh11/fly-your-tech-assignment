from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import app as graph_app
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fly Your Tech AI Chatbot")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to interact with the LangGraph chatbot.
    """
    try:
        # Run the graph with the user input
        initial_state = {"messages": [HumanMessage(content=request.message)]}
        result = graph_app.invoke(initial_state)
        
        # Get the last message content (the AI's response)
        final_message = result["messages"][-1].content
        return {"response": final_message}
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {"response": f"Backend Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
