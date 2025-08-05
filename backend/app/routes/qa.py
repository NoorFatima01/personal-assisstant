from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from app.dependencies.auth import verify_token
from app.schemas.qa_schema import QuestionRequest
from app.services.qa_services.streaming_rag_service import RAGService
import json


router = APIRouter()
rag_service = RAGService()

# non streaming endpoint
@router.post("/ask")
async def ask_question(question_request: QuestionRequest, user_id: str = Depends(verify_token)):
    question = question_request.question.strip()
    chat_id = question_request.chat_id
    week_start = question_request.week_start

    try:
        response = await rag_service.run_question(question, user_id, chat_id, week_start)
        return {"response": response}
    except Exception as e:
        print(f"Error during question answering: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": "InternalServerError"}
        )

# streaming endpoint
@router.post("/ask-stream")
async def ask_question_stream(
    question_request: QuestionRequest,
    user_id: str = Depends(verify_token)
):
    question = question_request.question.strip()
    chat_id = question_request.chat_id
    week_start = question_request.week_start

    try:
        stream = rag_service.run_question_streaming(question, user_id, chat_id, week_start)

        return StreamingResponse(stream, media_type="text/event-stream") 
    except Exception as e:
        print(f"Streaming error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "type": "InternalServerError"}
        )