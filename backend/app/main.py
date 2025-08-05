from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user import router as user_router
from app.routes.doc import router as doc_router
from app.routes.qa import router as qa_router
from app.routes.user import router as user_router

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
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(user_router, prefix="/api/auth", tags=["Auth"])
app.include_router(doc_router, prefix="/api/docs", tags=["Docs"])
app.include_router(qa_router, prefix="/api/qa", tags=["QA"])

# Error handling
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RAGException, rag_exception_handler)

