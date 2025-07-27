from fastapi import APIRouter, Depends
from app.dependencies.auth import verify_token
from backend.app.schemas.user_schema import UserProfile
from app.services.user_services import update_user_metadata


router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_current_user_info(userId: str = Depends(verify_token)):
    return {"id": userId}

