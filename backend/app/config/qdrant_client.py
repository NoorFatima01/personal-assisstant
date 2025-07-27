import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant as QdrantStore
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

if not all([QDRANT_URL, QDRANT_API_KEY]):
    raise ValueError("Missing Qdrant environment variables.")

# Connect to Qdrant Cloud
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Helper function to get vectorstore
def get_user_vector_store(user_id: str):
    embeddings = OpenAIEmbeddings()
    return QdrantStore(
        client=qdrant_client,
        collection_name=f"user_{user_id}_docs",
        embeddings=embeddings
    )
