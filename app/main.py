from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.agent.agent import run_agent
import traceback
app = FastAPI(title="SHL Agentic Recommender")

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "SHL Assessment Recommender API"}

# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
#     try:
#         result = run_agent(request.messages) 
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        result = run_agent(request.messages)
        return result
    except Exception as e:
        # This will print the exact red error trace to your terminal!
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))