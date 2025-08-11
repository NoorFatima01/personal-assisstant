from typing import Tuple, List
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.qdrant_client import get_user_vector_store



class QdrantVectorStoreEmbedService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
    
    def embed_documents(self, file_paths: List[Tuple[str, str]], user_id: str, week_start: str) -> None:
        documents = []
        
        for file_path, file_type in file_paths:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            for doc in docs:
                doc.metadata['file_type'] = file_type
                doc.metadata['week_start'] = week_start
                
            documents.extend(docs)

        split_docs = self.text_splitter.split_documents(documents)
        vectorstore = get_user_vector_store(user_id)
        vectorstore.add_documents(split_docs)