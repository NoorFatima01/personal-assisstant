from fastapi import APIRouter, Depends
from app.dependencies.auth import verify_token
from app.schemas.user_schema import UserProfile
from app.services.user_services.user_db_service import UserDBService


router = APIRouter()
user_db_service = UserDBService()



@router.get("/me", response_model=UserProfile)
def get_current_user_info(userId: str = Depends(verify_token)):
    user = user_db_service.get_user(userId)
    return user

