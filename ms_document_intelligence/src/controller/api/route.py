from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from ms_document_intelligence.src.usecase.document_usecase import analyze_document_usecase
from datetime import datetime
import tempfile
import os
import logging
import aiofiles

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/embedd_documents")
async def embedd_documents(
    file: UploadFile = File(...)
    ):

    allowed_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file type. Only PDF and DOCX files are allowed."
        )
    
    hours_and_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        suffix = "." + file.filename.split(".")[-1] if "." in file.filename else ""
        # Cria nome customizado: nome original + data/hora
        base_name = file.filename.rsplit('.', 1)[0] if '.' in file.filename else file.filename
        custom_name = f"{base_name}_{hours_and_date}{suffix}"
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, custom_name)
        async with aiofiles.open(temp_file_path, "wb") as tmp:
            await tmp.write(await file.read())
        logging.info(f"Temporary file created at: {temp_file_path}")

        classify, ocr = analyze_document_usecase(temp_file_path)

        os.remove(temp_file_path)  # Clean up the temporary file
    
        return {
            "classification": classify,
            "ocr": ocr        
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}"
        )

        

