from ms_document_intelligence.src.service.document_intelligence_service import classify_document_service, ocr_service

def analyze_document_usecase(document_path):
    classification_result = classify_document_service(document_path)
    print("Classification Result:", classification_result)

    ocr_result = ocr_service(document_path)
    print("OCR Result:", ocr_result)