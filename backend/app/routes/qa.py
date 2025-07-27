from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.dependencies.auth import verify_token
from app.schemas import QuestionRequest
from app.services.qa_services.qa_services import StreamingRAGService
import uuid


router = APIRouter()
rag_service = StreamingRAGService()

@router.post("/ask/stream")
async def stream_answer(request: QuestionRequest, user_id: str = Depends(verify_token)):
    request_id = str(uuid.uuid4())
    question = request.question.strip()

    async def event_generator():
        try:
            async for chunk in rag_service.stream_question(question, user_id, request_id):
                # If the client closes connection, stop streaming
                if await request.is_disconnected():
                    break

                yield {
                    "event": chunk["type"],
                    "data": chunk
                }
        except Exception as e:
            yield {
                "event": "error",
                "data": {
                    "error": str(e),
                    "type": "InternalServerError"
                }
            }
    return StreamingResponse(event_generator(), media_type="text/event-stream")