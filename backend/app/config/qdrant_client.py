import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant as QdrantStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client.models import VectorParams
from qdrant_client.models import PayloadSchemaType

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


if not all([QDRANT_URL, QDRANT_API_KEY]):
    raise ValueError("Missing Qdrant environment variables.")

# Connect to Qdrant Cloud
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def check_index_exists(client: QdrantClient, collection_name: str, field_name: str) -> bool:
    """Check if an index exists for a given field in the collection."""
    try:
        collection_info = client.get_collection(collection_name)

        # Check payload schema for the field
        if hasattr(collection_info, 'payload_schema') and collection_info.payload_schema:
            # payload_schema is a dict where keys are field names
            exists = field_name in collection_info.payload_schema
            print(f"Index check for '{field_name}': {'EXISTS' if exists else 'NOT FOUND'}")
            return exists

        return False
        
    except Exception as e:
        print(f"Error checking index for {field_name}: {e}")
        return False

def setup_qdrant_index(client: QdrantClient, collection_name: str):
    """Create index for file_type metadata field"""
    try:
        required_indexes = ["file_type", "week_start"]
        for field_name in required_indexes:
            if not check_index_exists(client, collection_name, field_name):
                client.create_payload_index(collection_name, field_name=field_name, field_schema=PayloadSchemaType.KEYWORD)
                print(f"Created index for '{field_name}' field in collection '{collection_name}'")

    except Exception as e:
        print(f"Error creating index: {e}")
        # Index might already exist, which is fine
        if "already exists" not in str(e).lower():
            raise

# Helper function to get vectorstore
def get_user_vector_store(user_id: str) -> QdrantStore:
    collection_name = f"user_{user_id}_docs"

    try:
        collection_info = qdrant_client.get_collection(collection_name)
        print(f"Collection {collection_name} already exists.")
        print(f"Collection info: {collection_info}")
    except Exception as e:
        print(f"Collection {collection_name} does not exist, creating it.")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance="Cosine",
            )
        )
        setup_qdrant_index(qdrant_client, collection_name)

    return QdrantStore(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embeddings
    )
