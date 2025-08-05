from app.config.supabase_client import supabase


class UserDBService:
    def __init__(self):
        self.supabase = supabase
        self.table_name = "users"

    def get_user(self, user_id: str) -> dict:
        """Get a user by ID"""
        response = self.supabase.table(self.table_name).select("*").eq("id", user_id).single().execute()
        if response.data is None:  # Check if no data was returned
            raise ValueError(f"User not found: {user_id}")
        return response.data

    def update_user(self, user_id: str, user_data: dict) -> dict:
        """Update an existing user"""
        response = self.supabase.table(self.table_name).update(user_data).eq("id", user_id).single().execute()
        if response.data is None:
            raise ValueError(f"Failed to update user: {user_id}")
        return response.data

    def delete_user(self, user_id: str) -> dict:
        """Delete a user by ID"""
        response = self.supabase.table(self.table_name).delete().eq("id", user_id).single().execute()
        return response.data

    def update_user_weeks(self, user_id: str, newWeek: str) -> dict:
        """Update the weeks for a user"""
        userData = self.get_user(user_id)
        if not userData:
            raise ValueError("User not found")
        weeks = userData.get("weeks")
        if not weeks:
            weeks = [newWeek]
        elif newWeek not in weeks:
            weeks.append(newWeek)
        response = self.supabase.table(self.table_name).update({"weeks": weeks}).eq("id", user_id).execute()
        return response.data