from fastapi import FastAPI
from ms_langgraph_agents.controller.route import router

app = FastAPI()

app.include_router(router, prefix="/ms_langgraph_agents", tags=["LangGraph Agents"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)