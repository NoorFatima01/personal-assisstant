from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RAG_RETRIEVAL_K: int = Field(2, description="Number of documents to retrieve for RAG")
    RAG_CLASSIFICATION_TEMP: float = Field(0.0, description="Temperature for classification LLM")
    RAG_GENERATION_TEMP: float = Field(0.1, description="Temperature for generation LLM")
    RAG_MAX_QUESTION_LENGTH: int = Field(1000, description="Max length of incoming question")
    RAG_CLASSIFICATION_RETRIES: int = Field(2, description="How many times to retry classification on error")
    RAG_CACHE_TTL: int = Field(300, description="Cache time-to-live in seconds")
    RAG_STREAMING_DELAY_MS: int = Field(100, description="Delay in milliseconds between streaming tokens")
    RAG_MAX_CONCURRENT_STREAMS: int = Field(10, description="Max concurrent streaming requests to prevent overload")
    CLASSIFICATION_PROMPT: str = Field("""
        You are a helpful assistant. Your task is to classify a user’s question into EXACTLY ONE of the following categories:

        - work: Job tasks, meetings, deadlines, career, professional development
        - health: Exercise, nutrition, medical, fitness, sports, wellness
        - personal: Family, friends, home, hobbies, casual activities (like drawing, painting, learning a language, learning art skills and coloring), self development activities, relaxing activities, social activities, daily tasks, house chores
        - reflection: Emotions, thoughts, self-analysis, mood, feelings, introspection

        Here are a few examples:

        Example 1:
        Question: What are my meetings this week?
        Category: work

        Example 2:
        Question: When should I go for a walk to stay active?
        Category: health

        Example 3:
        Question: How have I scheduled some time for painting at home?
        Category: personal

        Example 4:
        Question: I’ve been feeling anxious lately—what could be causing it?
        Category: reflection

        Now classify the question provided by the user:

        Respond with only one word — the category name:
""", description="Prompt for classification LLM to categorize user questions")
    GENERATION_PROMPT: str = Field(  """
                You are an intelligent personal assistant helping a user with questions about their life, work, health, and personal goals.

                The context below comes from the user's personal documents, tagged with file types:
                - work: Professional tasks, meetings, career-related content
                - health: Fitness, nutrition, medical information, wellness
                - personal: Family, friends, hobbies, daily life, social activities  
                - reflection: Thoughts, emotions, self-analysis, mood tracking

                If no relevant context is found, politely explain that you don't have enough information in their personal knowledge base to answer the question, and suggest they might want to add more relevant documents.
                Chat history is: 
                {chat_history}
                Context:
                {context}

                Question will be provided by the user, and you should answer based on the context provided. If the context is insufficient, be honest about the limitations.

                Answer:
                """, description="Prompt for generation LLM to answer user questions based on context")

# Singleton accessor
def get_settings() -> Settings:
    return Settings()
