from ms_document_intelligence.src.infrastructure.connection_blob_storage import ConnectionBlobStorage
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

blob_service_client = ConnectionBlobStorage.connect_blob_storage()

def create_dir_service(container_name, dir_name):
    """
    Create a directory in the specified container in Azure Blob Storage.
    """

    container_client = blob_service_client.get_container_client(container_name)
    
    blob_client = container_client.get_blob_client(f"{dir_name}/")
    blob_client.upload_blob(b"", overwrite=True)
    
    return f"Directory '{dir_name}' created in container '{container_name}'."

def list_directories_service(container_name):
    """
    List all directories in the specified container in Azure Blob Storage.
    """

    container_client = blob_service_client.get_container_client(container_name)
    
    directories = []
    blobs = container_client.list_blobs()
    
    for blob in blobs:
        if blob.name.endswith('/'):
            directories.append(blob.name)
    
    return directories

def create_directory_service(container_name, dir_name):
    """
    Create a directory in the specified container in Azure Blob Storage.
    """

    container_client = blob_service_client.get_container_client(container_name)
    
    blob_client = container_client.get_blob_client(f"{dir_name}/")
    blob_client.upload_blob(b"", overwrite=True)
    
    return f"Directory '{dir_name}' created in container '{container_name}'."

def upload_file_service(container_and_dir, file_path, blob_name):
    """
    Upload a file to the specified container and directory in Azure Blob Storage.
    """
    parts = container_and_dir.split('/', 1)
    container_name = parts[0]
    blob_dir = parts[1].strip('/') if len(parts) > 1 and parts[1].strip() else ""

    container_client = blob_service_client.get_container_client(container_name)
    if blob_dir:
        blob_path = f"{blob_dir}/{blob_name}"
    else:
        blob_path = blob_name

    with open(file_path, "rb") as data:
        container_client.upload_blob(name=blob_path, data=data, overwrite=True)

    return f"File '{file_path}' uploaded to container '{container_name}' in directory '{blob_dir}' as '{blob_name}'."

def create_directory_if_not_exists_service(container_name: str):
    """
    Create a directory in the blob storage if it does not already exist.
    """

    date_actual = datetime.today().strftime('%Y-%m-%d')
    container = container_name
    dir_exist_in_container = [d.strip('/').lower() for d in list_directories_service(container)]
    if date_actual.lower() not in dir_exist_in_container:
        create_directory_service(container, f"{date_actual}/")
        logging.info(f"Directory '{container}/{date_actual}/' created in container {container}.")
    else:
        logging.info(f"Directory '{container}/{date_actual}/' already exists in container {container}.")
    
    path_blob = f"{container}/{date_actual}/"
    return path_blob