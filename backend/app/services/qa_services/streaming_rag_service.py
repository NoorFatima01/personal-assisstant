from operator import itemgetter
from typing import AsyncGenerator, List
from langchain_core.runnables import RunnableParallel
from app.config.qdrant_client import get_user_vector_store
from app.config.settings import get_settings
from .question_classifier_service import QuestionClassifier
from .retrieval_engine_service import RetrievalEngine
from .response_generator_service import ResponseGenerator
from app.config.model_loader import get_llm_manager
from app.services.chat_services.chat_db_service import ChatDBService
# from app.utils.redis_cache import RedisCache
# from app.config.redis_client import redis_client


#  TODO: change this incorporate multiple classification categories


settings = get_settings()

class RAGConfig:
    def __init__(self):
        self.retrieval_k = settings.RAG_RETRIEVAL_K
        self.classification_temp = settings.RAG_CLASSIFICATION_TEMP
        self.generation_temp = settings.RAG_GENERATION_TEMP
        self.max_question_length = settings.RAG_MAX_QUESTION_LENGTH
        self.classification_retries = settings.RAG_CLASSIFICATION_RETRIES
        self.cache_ttl = settings.RAG_CACHE_TTL
        self.streaming_delay_ms = settings.RAG_STREAMING_DELAY_MS
        self.max_concurrent_streams = settings.RAG_MAX_CONCURRENT_STREAMS
        self.classification_prompt = settings.CLASSIFICATION_PROMPT
        self.generation_prompt = settings.GENERATION_PROMPT


class RAGService:
    """Streaming RAG service using LangChain Runnable chains for real-time responses"""
    
    def __init__(self):
        self.config = RAGConfig()
        # self.redis_cache = RedisCache(redis_client)
        
        # Stats tracking
        # self.stats = {
        #     "active_streams": 0,
        #     "total_streamed": 0,
        #     "total_chunks_sent": 0
        # }

    def _build_sync_chain(self, user_id: str, chat_id: str, week_start: List[str]):
        """Build a sync Runnable chain for non-streaming chat"""
        try:
            chat_service = ChatDBService()
            vectorstore = get_user_vector_store(user_id)

            llm_manager = get_llm_manager()
            shared_llm = llm_manager.shared_llm
            classifier = QuestionClassifier(shared_llm, self.config.classification_prompt)
            retriever = RetrievalEngine(vectorstore, self.config.retrieval_k)
            generator = ResponseGenerator(shared_llm, self.config.generation_prompt, chat_service, user_id, chat_id)

            chain = (
                RunnableParallel({
                    "question": itemgetter("question"),
                    "week_start": itemgetter("week_start"),
                    "classification": itemgetter("question") | classifier.as_runnable()
                })
                | retriever.as_runnable()
                | generator.as_runnable()
            )

            return chain
        except Exception as e:
            print("Error building sync chain:", e)
            raise

    async def run_question_streaming(
        self, question: str, user_id: str, chat_id: str, week_start: List[str]
    ) -> AsyncGenerator[str, None]:
        """Stream response chunks as Server-Sent Events"""
        try:
            chain = self._build_sync_chain(user_id, chat_id, week_start)

            async for chunk in chain.astream({
                "question": question,
                "week_start": week_start
            }):
                if isinstance(chunk, dict):
                    text = chunk.get("output", "")
                elif isinstance(chunk, str):
                    text = chunk
                else:
                    text = ""
                
                # Escape newlines to ensure single SSE message
                text = text.replace("\n", "\\n")
                yield f"data: {text}\n\n"

        except Exception as e:
            print(f"Error during streaming RAG: {str(e)}")
            yield f"data: Something went wrong during streaming.\n\n"




    # async def run_question(self, question: str, user_id: str, chat_id: str, week_start: List[str]) -> str:
    #     """Process a question synchronously (non-streaming)"""
    #     try:
    #         print(f"Running sync RAG for user {user_id}, chat {chat_id}")
    #         chain = self._get_cached_chain(user_id, chat_id, week_start)
    #         response = await chain.ainvoke({
    #             "question": question,
    #             "week_start": week_start
    #         })
    #         return response
    #     except Exception as e:
    #         print(f"Error during non-streaming RAG processing: {str(e)}")
    #         return "Something went wrong. Please try again later."


    # def _get_cached_chain(self, user_id: str, chat_id: str, week_start: List[str]):
    #     chain_key = self.redis_cache.make_key("chain", user_id, chat_id)
    #     chain = self.redis_cache.get(chain_key)
    #     if chain:
    #         return chain
    #     # If not cached, build the chain
    #     chain = self._build_sync_chain(user_id, chat_id, week_start)
    #     self.redis_cache.set_pickle(chain_key, chain, ttl=self.config.cache_ttl)
    #     return chain