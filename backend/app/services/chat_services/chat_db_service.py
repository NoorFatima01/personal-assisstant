from typing import Optional, Tuple, List
from app.config.supabase_client import supabase
from fastapi import HTTPException


class ChatDBService:
    def __init__(self, table_name: str = "chats"):
        self.table_name = table_name
        self.supabase = supabase

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
            print(f"Fetching chat session for chat_id: {chat_id}")
            response = self.supabase.table(self.table_name).select("*").eq("id", chat_id).execute()
            print(f"Response from database: {response}")

            if not response.data:
                response = self.supabase.table(self.table_name).insert({
                "user_id": user_id,
                "id": chat_id,
                "messages": [],
                "status": "active",
                "messages_count": 0,
                }).execute()
            print(f"Chat session created data: {response.data}")
            if response.data:
                return response.data[0]
            else:
                raise HTTPException(status_code=404, detail="Chat session not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
    def update_chat_session(self, chat_id: str, newMessages: List[dict]) -> None:
        try:
            print(f"Updating chat session {chat_id} with new messages: {newMessages}")
            response = self.supabase.table(self.table_name).select("messages").eq("id", chat_id).single().execute()
            if not response.data:
                raise HTTPException(status_code=404, detail="Chat session not found")
            
            existing_messages = response.data["messages"] or []
            updated_messages = existing_messages + newMessages
            updated_count = len(updated_messages)

            updated_data = {
                "messages": updated_messages,
                "messages_count": updated_count
            }

            print(f"Updating chat session {chat_id} with {updated_count} messages")

            self.supabase.table(self.table_name).update(updated_data).eq("id", chat_id).execute()

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database update error: {str(e)}")