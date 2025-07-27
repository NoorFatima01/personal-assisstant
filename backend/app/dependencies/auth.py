from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import  supabase

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
        user = response.user

        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user.id  # ✅ Return only user ID

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token verification failed.")