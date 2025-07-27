from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    RAG_RETRIEVAL_K: int = Field(8, description="Number of documents to retrieve for RAG")
    RAG_CLASSIFICATION_TEMP: float = Field(0.0, description="Temperature for classification LLM")
    RAG_GENERATION_TEMP: float = Field(0.1, description="Temperature for generation LLM")
    RAG_MAX_QUESTION_LENGTH: int = Field(1000, description="Max length of incoming question")
    RAG_CLASSIFICATION_RETRIES: int = Field(2, description="How many times to retry classification on error")
    RAG_LLM_MODEL: str = Field("gpt-4", description="Model to use for LLM calls")
    RAG_CACHE_TTL: int = Field(300, description="Cache time-to-live in seconds")
    RAG_STREAMING_DELAY_MS: int = Field(100, description="Delay in milliseconds between streaming tokens")
    RAG_MAX_CONCURRENT_STREAMS: int = Field(10, description="Max concurrent streaming requests to prevent overload")
    CLASSIFICATION_PROMPT: str = Field("""
                Classify the following user question into EXACTLY ONE of these categories: work, health, personal, reflection
                
                Guidelines:
                - work: Job tasks, meetings, deadlines, career, professional development
                - health: Exercise, nutrition, medical, fitness, sports, wellness
                - personal: Family, friends, home, hobbies, social activities, daily tasks
                - reflection: Emotions, thoughts, self-analysis, mood, feelings, introspection
                
                Question: {question}
                
                Respond with ONLY the category name (work/health/personal/reflection):
            """, description="Prompt for classification LLM to categorize user questions")
    GENERATION_PROMPT: str = Field(  """
                You are an intelligent personal assistant helping a user with questions about their life, work, health, and personal goals.

                The context below comes from the user's personal documents, tagged with file types:
                - work: Professional tasks, meetings, career-related content
                - health: Fitness, nutrition, medical information, wellness
                - personal: Family, friends, hobbies, daily life, social activities  
                - reflection: Thoughts, emotions, self-analysis, mood tracking

                If no relevant context is found, politely explain that you don't have enough information in their personal knowledge base to answer the question, and suggest they might want to add more relevant documents.

                Context:
                {context}

                Question: {question}

                Please provide a helpful, personalized answer based on the context above. If the context is insufficient, be honest about the limitations.

                Answer:
                """, description="Prompt for generation LLM to answer user questions based on context")

# Singleton accessor
def get_settings() -> Settings:
    return Settings()
