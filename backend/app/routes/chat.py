from fastapi import APIRouter, Depends
from gotrue import List
from app.dependencies.auth import verify_token
from app.services.chat_services.chat_db_service import ChatDBService
from app.schemas.chat_schema import ChatResponseModel
from fastapi.responses import JSONResponse


router = APIRouter()
chat_db_service = ChatDBService()

@router.get("/my-chats", response_model=List[ChatResponseModel])
async def get_user_chats(user_id: str = Depends(verify_token)):

    try:
        chat_sessions = chat_db_service.get_user_chats(user_id)
        return JSONResponse(
            content={
                "data": chat_sessions,
                "message": "User chat sessions retrieved successfully",
                "status": "success"
            },
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                "data": None,
                "message": f"Error retrieving user chat sessions: {str(e)}",
                "status": "error"
            },
            status_code=500
        )

@router.get("/my-chats/{chat_id}", response_model=ChatResponseModel)
async def get_chat_session(chat_id: str, user_id: str = Depends(verify_token)):

    try:
        chat_session = chat_db_service.get_chat_session(user_id, chat_id)
        return JSONResponse(
                content={
                    "data": chat_session,
                    "message": "Chat session retrieved successfully",
                    "status": "success"
                },
                status_code=200
            )
    except Exception as e:
        return JSONResponse(
            content={
                "data": None,
                "message": f"Error retrieving chat session: {str(e)}",
                "status": "error"
            },
            status_code=500
        )
