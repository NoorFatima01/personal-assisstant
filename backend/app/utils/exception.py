from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from datetime import datetime

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

# Custom Exceptions
class RAGException(Exception):
    """Base RAG exception"""
    pass

class ClassificationException(RAGException):
    """Exception raised when question classification fails"""
    pass

class RetrievalException(RAGException):
    """Exception raised when document retrieval fails"""
    pass

class GenerationException(RAGException):
    """Exception raised when answer generation fails"""
    pass

async def rag_exception_handler(request: Request, exc: RAGException):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
            "timestamp": datetime.now().isoformat()
        }
    )

