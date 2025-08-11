from typing import Optional, List
from app.config.supabase_client import supabase
from fastapi import HTTPException


class ChatDBService:
    def __init__(self):
        self.table_name = "chats"
        self.supabase = supabase
    
    def get_chat_session(self, user_id:str, chat_id:str) -> Optional[dict]:
        try:
            response = self.supabase.table(self.table_name).select("*").eq("id", chat_id).eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    def create_chat_session(self, user_id: str, chat_id: str, messages: List[dict]) -> None:
        try:
            messages_count = len(messages)
            self.supabase.table(self.table_name).insert({
                "user_id": user_id,
                "id": chat_id,
                "messages": messages,
                "status": "active",
                "messages_count": messages_count,
            }).execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database insert error: {str(e)}")

    def get_or_create_chat_session(self, chat_id: str, user_id: str) -> dict:
        try:
            response = self.supabase.table(self.table_name).select("*").eq("id", chat_id).execute()

            if not response.data:
                response = self.supabase.table(self.table_name).insert({
                "user_id": user_id,
                "id": chat_id,
                "messages": [],
                "status": "active",
                "messages_count": 0,
                }).execute()
            if response.data:
                return response.data[0]
            else:
                raise HTTPException(status_code=404, detail="Chat session not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    def update_chat_session(self, chat_id: str, newMessages: List[dict]=None, status: str = None) -> None:
        try:
            response = self.supabase.table(self.table_name).select("messages").eq("id", chat_id).single().execute()
            if not response.data:
                raise ValueError("Chat session not found")
            
            updated_data = {}
            if newMessages:
                existing_messages = response.data["messages"] or []
                updated_messages = existing_messages + newMessages
                updated_count = len(updated_messages)

                updated_data = {
                    "messages": updated_messages,
                    "messages_count": updated_count
                }

            if status:
                updated_data["status"] = status

            self.supabase.table(self.table_name).update(updated_data).eq("id", chat_id).execute()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")
        
    def get_user_chats(self, user_id:str) -> List[dict]:
        try:
            response = self.supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
            if response.data:
                return response.data
            else:
                return None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")