from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import uuid
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

class ConnectionBlobStorage:
    
    @staticmethod
    def connect_blob_storage():    
        account_url = os.getenv("URL_BLOB_STORAGE")
        default_credential = DefaultAzureCredential()

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        return blob_service_client