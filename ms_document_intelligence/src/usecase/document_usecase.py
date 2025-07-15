from ms_document_intelligence.src.service.document_intelligence_service import classify_document_service, ocr_service
from ms_document_intelligence.src.service.blob_storage_service import create_directory_if_not_exists_service, upload_file_service
import logging

logging.basicConfig(level=logging.INFO)

def analyze_document_usecase(document_path):

    classification_result = classify_document_service(document_path)
    logging.info(f"Classification Result: {classification_result}")

    path_blob = create_directory_if_not_exists_service(classification_result["classify_type"])

    print(upload_file_service(path_blob, document_path, document_path.split("/")[-1]))

    ocr_result = ocr_service(document_path)
    logging.info(f"OCR Result: {ocr_result}")

    return classification_result["classify_type"], ocr_result