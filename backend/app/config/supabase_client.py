import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not all([SUPABASE_URL, SUPABASE_ANON_KEY]):
    raise ValueError("Missing environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
