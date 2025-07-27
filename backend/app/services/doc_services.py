from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.qdrant_client import get_user_vector_store
from typing import List
from app.config.supabase_client import supabase
from fastapi import HTTPException


def upload_to_supabase_bucket(file_path: str, user_id: str, file_type: str):
    bucket_name = "patient-pdfs"
    storage_path = f"{user_id}/{file_type}_{file_path.split('/')[-1]}"
    
    try:

        with open(file_path, "rb") as file:
            response = supabase.storage.from_(bucket_name).upload(storage_path, file)
        if response.error:
            raise Exception(response.error.message)

        public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path).public_url
        return public_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase upload error: {str(e)}")


def load_and_embed_doc(file_paths:List[str], user_id:str):
    documents = []
    for file_path, file_type in file_paths:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        for doc in docs:
            doc.metadata['file_type'] = file_type
        documents.extend(docs)

    # splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)

    vectorstore = get_user_vector_store(user_id)
    vectorstore.add_documents(split_docs)




