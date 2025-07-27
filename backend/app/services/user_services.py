from app.config.supabase_client import supabase

def update_user_metadata(user_id: str, metadata: dict):
    response = supabase.auth.admin.update_user_by_id(user_id, {"user_metadata": metadata})
    if response.user:
        return {
            "message": "Profile updated successfully",
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "user_metadata": response.user.user_metadata
            }
        }
    raise Exception("Failed to update user")
