from ms_document_intelligence.src.infrastructure.connection_document_intelligence import ConnectionDocumentIntelligence
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import requests
from dotenv import load_dotenv
import os

load_dotenv()

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

def send_to_agents_service(ocr_document, type_document, documents_name):
    base_url= os.getenv("BASE_URL_AGENT_LANGGRAPH")
    if type_document == "contratos":
        url = f"{base_url}/ms_langgraph_agents/contracts"
        json = {
                "text": f"{ocr_document}",
                "documents_name": documents_name
                }
        request = requests.post(
            url= url,
            json=json
        )
    else:
        url = f"{base_url}/ms_langgraph_agents/documents"
        json = {
                "text": f"{ocr_document}",
                "documents_name": documents_name
                }
        request = requests.post(    
            url= url,
            json=json
        )


#classify_document_service("/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions/arquivos-teste/documentos-processuais/Despacho_Judicial_Designação_de_Audiência.docx")
#print(ocr_service("/Users/leonardojdss/Desktop/projetos/AI-Document-Architecture-Solutions/arquivos-teste/contratos/Contrato_de_Representação_Comercial.docx"))