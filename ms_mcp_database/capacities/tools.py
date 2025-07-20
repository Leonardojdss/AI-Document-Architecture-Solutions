from mcp.server.fastmcp import FastMCP, Context
from ms_mcp_database.infrastructure.postgrsql_connection import PostgreSQLConnection
from ms_mcp_database.infrastructure.connection_blob_storage import ConnectionBlobStorage
from ms_mcp_database.model.table_model import Document, Contract
from typing import Literal
from datetime import date, datetime
import logging
import json

logging.basicConfig(level=logging.INFO)
mcp = FastMCP()
db = PostgreSQLConnection()
blob_service_client = ConnectionBlobStorage.connect_blob_storage()

@mcp.tool()
def list_archives_blob(container_name: str, date: str = None) -> str:
    
    try:
        container_client = blob_service_client.get_container_client(container=container_name)
        blob_list = container_client.list_blobs()
        filtered_blobs = []
        for blob in blob_list:
            if date is None or date in blob.name:
                filtered_blobs.append(blob.name)
        return str(filtered_blobs)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def save_analyze_to_db(table_name: Literal["documents", "contracts"], document_name: str, analyze_data: str) -> str:
    session = db.get_session()
    analyze_date = date.today()
    try:
        if table_name == "documents":
            obj = Document(date=analyze_date, document_name=document_name, resume_ai=analyze_data)
        elif table_name == "contracts":
            obj = Contract(date=analyze_date, document_name=document_name, resume_ai=analyze_data)
        else:
            return "Invalid table name"
        session.add(obj)
        session.commit()
        return f"Inserted into {table_name} with id {obj.id}"
    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"
    finally:
        session.close()

@mcp.tool()
def query_data_from_db(table_name: Literal["documents", "contracts"], date: str) -> str:
    session = db.get_session()
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        
        if table_name == "documents":
            results = session.query(Document).filter(Document.date == date_obj).all()
        elif table_name == "contracts":
            results = session.query(Contract).filter(Contract.date == date_obj).all()
        else:
            return "Invalid table name"
        
        if results:
            output = [
                {
                    "data": str(row.date),
                    "nome_documento": row.document_name,
                    "analise": row.resume_ai
                }
                for row in results
            ]
            return json.dumps(output, ensure_ascii=False)
        else:
            return json.dumps({"error": f"No records found in {table_name} for date: {date}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
    finally:
        session.close()