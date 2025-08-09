from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.dependencies.auth import verify_token
from app.schemas.user_schema import UserProfileResponse
from app.services.user_services.user_db_service import UserDBService


router = APIRouter()
user_db_service = UserDBService()

@router.get("/me", response_model=UserProfileResponse)
def get_current_user_info(userId: str = Depends(verify_token)):
    try:
        user = user_db_service.get_user(userId)
        return JSONResponse(
            content={
                "data": user,
                "message": "User retrieved successfully",
                "status": "success"
            }, 
            status_code=200
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

