from fastapi import APIRouter, HTTPException
from ms_langgraph_agents.usecase.conversation_usecase import conversation_contracts_usecase, conversation_documents_usecase
from pydantic import BaseModel
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
class TextInput(BaseModel):
    text: str
    documents_name: Optional[str] = None

router = APIRouter()

@router.post("/documents")
async def documents_route(data: TextInput):
    
    text = data.text
    document_name = f"nome do documento: {data.documents_name}"
    text_input = f"{text} {document_name}"
    if not text_input.strip():
        raise HTTPException(
            status_code=400,
            detail="Requisição vazia, valide os campos enviados."
        )
    
    try:
        response = await conversation_documents_usecase(text_input)
        logging.info(f"Response from documents use case: {response}")
        return {"response_agents": response}
    except Exception as e:
        logging.error(f"Error in documents route: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a requisição: {str(e)}"
        )
    
@router.post("/contracts")
async def contracts_route(data: TextInput):
    
    text = data.text
    documents_name = f"nome do documento: {data.documents_name}"
    text_input = f"{text} {documents_name}"
    if not text_input.strip():
        raise HTTPException(
            status_code=400,
            detail="Requisição vazia, valide os campos enviados."
        )
    
    try:
        response = await conversation_contracts_usecase(text_input)
        logging.info(f"Response from contracts use case: {response}")
        return {"response_agents": response}
    except Exception as e:
        logging.error(f"Error in contracts route: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a requisição: {str(e)}"
        )
    