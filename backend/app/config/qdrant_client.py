import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant as QdrantStore
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client.models import VectorParams
from qdrant_client.models import PayloadSchemaType
from qdrant_client.models import OptimizersConfigDiff
from qdrant_client.http.models import PayloadSchemaType 


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
        
        if hasattr(collection_info, 'payload_schema') and collection_info.payload_schema:
            exists = field_name in collection_info.payload_schema
            return exists
        return False
        
    except Exception as e:
        print(f"Error checking index for {field_name}: {e}")
        return False

def setup_qdrant_index(client: QdrantClient, collection_name: str):
    """Create indexes for nested metadata fields"""
    try:
        # Use the correct nested field names
        required_indexes = ["metadata.file_type", "metadata.week_start"]

        for field_name in required_indexes:
            if not check_index_exists(client, collection_name, field_name):
                client.create_payload_index(
                    collection_name=collection_name,
                    field_name=field_name, 
                    field_schema=PayloadSchemaType.KEYWORD,
                    wait=True
                )
            else:
                # Index already exists, no action needed
                pass

    except Exception as e:
        if "already exists" not in str(e).lower():
            raise

def get_user_vector_store(user_id: str) -> QdrantStore:
    collection_name = f"user_{user_id}_docs"

    try:
        qdrant_client.get_collection(collection_name)

    except Exception as e:        
        # Create collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance="Cosine"
            ),
            optimizers_config=OptimizersConfigDiff(
                deleted_threshold=0.2,
                vacuum_min_vector_number=100,
                default_segment_number=0,
                indexing_threshold=4,
                flush_interval_sec=5
            )
        )
    
    # Always setup indexes (for both new and existing collections)
    setup_qdrant_index(qdrant_client, collection_name)

    return QdrantStore(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embeddings
    )