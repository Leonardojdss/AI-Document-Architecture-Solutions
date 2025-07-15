from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

endpoint = os.getenv("YOUR_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("YOUR_FORM_RECOGNIZER_KEY")

class ConnectionDocumentIntelligence:
    
    @staticmethod
    def connect_document_intelligence():
        if not endpoint or not key:
            raise ValueError("Endpoint and key must be set in environment variables.")
        
        # Create the Document Intelligence client
        document_intelligence_client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
        return document_intelligence_client