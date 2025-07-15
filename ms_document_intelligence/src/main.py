from fastapi import FastAPI
from ms_document_intelligence.src.controller.api.route import router

app = FastAPI()

app.include_router(router, prefix="/ms_document_intelligence", tags=["Document Intelligence"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)