from app.config.supabase_client import supabase


class NotificationDBService:
    def __init__(self):
        self.supabase = supabase
        self.table_name = "notifications"

    def create_notification(self, user_id: str, message: str) -> dict:
        """Create a new notification for a user"""
        response = self.supabase.table(self.table_name).insert({
            "user_id": user_id,
            "message": message
        }).execute()
        return response.data

    def get_notifications(self, user_id: str) -> list:
        """Get all notifications for a user"""
        response = self.supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
        return response.data if response.data else []

    def mark_notification_as_read(self, notification_id: str) -> dict:
        """Mark a notification as read"""
        response = self.supabase.table(self.table_name).update({"read": True}).eq("id", notification_id).execute()
        return response.data

    def send_notification(self, message: str, user_email: str, user_id: str) -> dict:
        """Send a notification to a user"""
        if not user_email:
            return {}
        return self.create_notification(user_id, message)