from langchain_groq.chat_models import ChatGroq

import os

class LLMManager:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.shared_llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.7,
        )


llm_manager_instance = None

def get_llm_manager():
    global llm_manager_instance
    if llm_manager_instance is None:
        llm_manager_instance = LLMManager()
    return llm_manager_instance
