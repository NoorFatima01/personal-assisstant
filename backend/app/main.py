from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.utils.exception import http_exception_handler
from app.utils.exception import rag_exception_handler, RAGException

app = FastAPI(title="FastAPI + Supabase Auth API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Routers
app.include_router(user.router, prefix="/auth", tags=["Auth"])
# app.include_router(data.router, prefix="/data", tags=["Data"])
# app.include_router(public.router, tags=["Public"])

# Error handling
app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(RAGException, rag_exception_handler)

