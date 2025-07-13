from ms_document_intelligence.src.infrastructure.connection_document_intelligence import ConnectionDocumentIntelligence
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import os

client = ConnectionDocumentIntelligence.connect_document_intelligence()

def classify_document_service(document_path):
    model_id = os.getenv("MODEL_ID")
    with open(document_path, "rb") as f:
        poller = client.begin_classify_document(
            model_id, AnalyzeDocumentRequest(bytes_source=f.read())
        )
    result = poller.result()
    result = result.as_dict()

    result_json = {
        "classify_type": result["documents"][0].get("docType"),
        "confidence": result["documents"][0].get("confidence"),
        "model_id": result["modelId"]
        }

    return result_json

  
def ocr_service(document_path):
    
    with open(document_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-read", AnalyzeDocumentRequest(bytes_source=f.read())
        )
        result = poller.result()
   
    return result.content


#classify_document_service("/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions/arquivos-teste/documentos-processuais/Despacho_Judicial_Designação_de_Audiência.docx")
print(ocr_service("/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions/arquivos-teste/contratos/Contrato_de_Representação_Comercial.docx"))