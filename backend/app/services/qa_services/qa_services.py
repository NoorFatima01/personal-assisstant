import asyncio
from datetime import time
from typing import Any, AsyncGenerator, Dict, Tuple
from langchain_core.runnables import RunnableMap, RunnableLambda, RunnablePassthrough
from app.config.qdrant_client import get_user_vector_store
from app.config.settings import get_settings
from app.utils.exception import RetrievalException, RAGException, GenerationException, ClassificationException
from rag_chains.classifier import QuestionClassifier
from rag_chains.retrieval_engine import RetrievalEngine
from rag_chains.response_generator import ResponseGenerator

#  TODO: change this incorporate multiple classification categories


settings = get_settings()

class RAGConfig:
    def __init__(self):
        self.retrieval_k = settings.RAG_RETRIEVAL_K
        self.classification_temp = settings.RAG_CLASSIFICATION_TEMP
        self.generation_temp = settings.RAG_GENERATION_TEMP
        self.max_question_length = settings.RAG_MAX_QUESTION_LENGTH
        self.classification_retries = settings.RAG_CLASSIFICATION_RETRIES
        self.llm_model = settings.RAG_LLM_MODEL
        self.cache_ttl = settings.RAG_CACHE_TTL
        self.streaming_delay_ms = settings.RAG_STREAMING_DELAY_MS
        self.max_concurrent_streams = settings.RAG_MAX_CONCURRENT_STREAMS
        self.classification_prompt = settings.CLASSIFICATION_PROMPT
        self.generation_prompt = settings.GENERATION_PROMPT


class StreamingRAGService:
    """Streaming RAG service using LangChain Runnable chains for real-time responses"""
    
    def __init__(self):
        self.config = RAGConfig()
        
        # Cache for streaming chains
        self.chain_cache: Dict[str, Tuple[Any, float]] = {}
        self.vectorstore_cache: Dict[str, Tuple[Any, float]] = {}
        
        # Stats tracking
        self.stats = {
            "active_streams": 0,
            "total_streamed": 0,
            "total_chunks_sent": 0
        }
    
    def _get_cached_vectorstore(self, user_id: str):
        """Get cached vectorstore or create new one"""
        if user_id in self.vectorstore_cache:
            vectorstore, timestamp = self.vectorstore_cache[user_id]
            if time.time() - timestamp < self.config.cache_ttl:
                return vectorstore
            else:
                del self.vectorstore_cache[user_id]
        
        vectorstore = get_user_vector_store(user_id)
        if vectorstore is None:
            raise RetrievalException(f"No vector store found for user {user_id}")
        
        self.vectorstore_cache[user_id] = (vectorstore, time.time())
        return vectorstore
    
    def _build_streaming_chain(self, user_id: str):
        """Build a streaming Runnable chain for the user"""
        try:
            vectorstore = self._get_cached_vectorstore(user_id)
        
            classifier = QuestionClassifier(self.config.llm_model, self.config.classification_temp, self.config.classification_prompt)
            retriever = RetrievalEngine(vectorstore, self.config.retrieval_k)
            generator = ResponseGenerator(self.config.llm_model, self.config.generation_temp, self.config.generation_prompt)
            
            # Build the complete chain
            chain = (
                RunnableMap({
                    "classification": classifier.as_runnable(),
                    "question": RunnablePassthrough()
                })
                | retriever.as_runnable()
                | generator.as_runnable()
            )
            
            return chain
            
        except Exception as e:
            print(f"Failed to build streaming chain for user {user_id}: {str(e)}")
            raise RAGException(f"Failed to build streaming RAG chain: {str(e)}")
    
    def _get_cached_chain(self, user_id: str):
        """Get cached streaming chain or build new one"""
        if user_id in self.chain_cache:
            chain, timestamp = self.chain_cache[user_id]
            if time.time() - timestamp < self.config.cache_ttl:
                return chain
            else:
                del self.chain_cache[user_id]
        
        chain = self._build_streaming_chain(user_id)
        self.chain_cache[user_id] = (chain, time.time())
        return chain
    
    async def stream_question(self, question: str, user_id: str, request_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream a question response using the Runnable chain"""
        self.stats["active_streams"] += 1
        chunks_sent = 0
        
        try:
            print(f"Starting streaming RAG for request {request_id}")
            
            # Send classification status
            yield {
                "type": "status",
                "message": "Understanding your question...",
                "step": "classification",
                "request_id": request_id
            }
            
            # Get or build streaming chain
            chain = self._get_cached_chain(user_id)
            
            # Send retrieval status
            yield {
                "type": "status", 
                "message": "Searching your documents...",
                "step": "retrieval",
                "request_id": request_id
            }
            
            # Initialize variables for streaming
            classification = "unknown"
            sources_count = 0
            accumulated_response = ""
            
            # Send generation status
            yield {
                "type": "status",
                "message": "Generating your personalized response...",
                "step": "generation", 
                "request_id": request_id
            }
            
            # Stream the response
            try:
                async for chunk in chain.astream({"question": question}):
                    if isinstance(chunk, dict):
                        classification = chunk.get("classification", "unknown")
                        sources_count = chunk.get("sources_count", 0)

                    if hasattr(chunk, 'content') and chunk.content:
                        content = chunk.content
                        accumulated_response += content
                        chunks_sent += 1
                        
                        yield {
                            "type": "chunk",
                            "content": content,
                            "request_id": request_id
                        }
                        
                        # Add small delay for better UX
                        if self.config.streaming_delay_ms > 0:
                            await asyncio.sleep(self.config.streaming_delay_ms / 1000)
                
                # Send metadata after streaming is complete
                yield {
                    "type": "metadata",
                    "classification": classification,
                    "sources_used": sources_count,
                    "total_chunks": chunks_sent,
                    "request_id": request_id
                }
                
                print(f"Streaming completed for request {request_id} - {chunks_sent} chunks sent")
                
            except GenerationException as e:
                print(f"Streaming generation failed for request {request_id}: {str(e)}")
                yield {
                    "type": "error",
                    "error": "I had trouble generating a response. Please try again.",
                    "error_type": "GenerationException",
                    "request_id": request_id
                }
                
        except ClassificationException as e:
            print(f"Streaming classification failed for request {request_id}: {str(e)}")
            yield {
                "type": "error",
                "error": "I couldn't understand your question. Could you rephrase it?",
                "error_type": "ClassificationException", 
                "request_id": request_id
            }
            
        except RetrievalException as e:
            print(f"Streaming retrieval failed for request {request_id}: {str(e)}")
            yield {
                "type": "error",
                "error": "I couldn't find relevant information in your documents.",
                "error_type": "RetrievalException",
                "request_id": request_id
            }
            
        except Exception as e:
            print(f"Streaming unexpected error for request {request_id}: {str(e)}")
            yield {
                "type": "error",
                "error": "An unexpected error occurred while processing your question",
                "error_type": "InternalError",
                "request_id": request_id
            }
            
        finally:
            self.stats["active_streams"] -= 1
            self.stats["total_streamed"] += 1
            self.stats["total_chunks_sent"] += chunks_sent
    
    def get_stats(self) -> Dict[str, Any]:
        """Get streaming service statistics"""
        return self.stats.copy()
    
    def clear_user_cache(self, user_id: str) -> bool:
        """Clear cache for a specific user"""
        cleared = False
        
        if user_id in self.chain_cache:
            del self.chain_cache[user_id]
            cleared = True
            
        if user_id in self.vectorstore_cache:
            del self.vectorstore_cache[user_id]
            cleared = True
            
        return cleared
    
    def clear_all_cache(self) -> int:
        """Clear all streaming caches"""
        total_count = len(self.chain_cache) + len(self.vectorstore_cache)
        self.chain_cache.clear()
        self.vectorstore_cache.clear()
        return total_count






# Legacy function for backward compatibility
# def build_rag_chain(user_id: str):
#     """
#     Legacy function for backward compatibility.
#     Consider migrating to RAGService.process_question() for new code.
#     """
#     logger.warning("build_rag_chain() is deprecated. Use RAGService.process_question() instead.")
    
#     # This is a simplified version that maintains the old interface
#     # but uses the new service internally
#     service = RAGService()
    
#     def legacy_chain_invoke(inputs):
#         import asyncio
#         question = inputs.get("question", "")
#         request_id = f"legacy_{int(time.time())}"
        
#         # Run the async method in sync context
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         try:
#             result = loop.run_until_complete(
#                 service.process_question(question, user_id, request_id)
#             )
#             return result
#         finally:
#             loop.close()
    
#     # Return a callable that mimics the old chain interface
#     class LegacyChain:
#         def invoke(self, inputs):
#             return legacy_chain_invoke(inputs)
    
#     return LegacyChain()
    






# class QuestionClassifier:
#     """Classifies user questions into categories for RAG processing. Has retry logic"""
#     def __init__(self, config:RAGConfig):
#         self.config = config
#         self.classification_prompt = PromptTemplate.from_template(
#             """
#             Classify the following user question into EXACTLY ONE of these categories: work, health, personal, reflection
            
#             Guidelines:
#             - work: Job tasks, meetings, deadlines, career, professional development
#             - health: Exercise, nutrition, medical, fitness, sports, wellness
#             - personal: Family, friends, home, hobbies, social activities, daily tasks
#             - reflection: Emotions, thoughts, self-analysis, mood, feelings, introspection
            
#             Question: {question}
            
#             Respond with ONLY the category name (work/health/personal/reflection):
#             """

#         )

#         self.llm = ChatOpenAI(
#             model_name=self.config.llm_model,
#             temperature=self.config.classification_temp,
#             max_tokens=50
#         )

#         self.chain = self.classification_prompt | self.llm | StrOutputParser()
#         self.valid_categories = {"work", "health", "personal", "reflection"}
#         self.fallback_category = "reflection" 

#         def classify_with_retry(self, question:str) -> ClassificationResult:
#             """"Classifies a question with retry logic and validation"""
#             attempts = 0 
#             try:
#                 while attempts < self.config.classification_retries:
#                     result = self.chain.invoke({"question":question})
#                     category = result.strip().lower()
#                     if category in self.valid_categories:
#                         return ClassificationResult(
#                             attempts=attempts + 1,
#                             category=category,
#                         )
#                     else:
#                         print(f"Invalid category '{category}' for question '{question}'. Attempt: {attempts + 1}")
#                         attempts += 1
#                 return ClassificationResult(
#                     attempts=attempts + 1,
#                     category=self.fallback_category
#                 )   
#             except Exception as e:
#                 print(f"Error occurred while classification. Attempt: {attempts + 1}: {e}")
#                 return ClassificationResult(
#                     attempts=attempts + 1,
#                     category=self.fallback_category
#                 )

# class DocumentRetriever:
#     def __init__(self, config:RAGConfig):
#         self.config = config

#     def get_boosted_retriever(self, vectorstore, file_type:str):
#         """"Create a metadata-aware retriever with error handling"""
#         try:
#             return vectorstore.as_retriever(
#                 search_kwargs={
#                     "k": self.config.retrieval_k,
#                     "filter": {"file_type": file_type}  # boost chunks from this file_type
#                 }
#             )
#         except Exception as e:
#             print(f"Error creating retriever for file type '{file_type}': {e}")
#             raise RetrievalException(f"Failed to create retriever for file type '{file_type}'") from e      

#     def get_fallback_retriever(self, vectorstore):
#         """Create a fallback retriever with no filters"""
#         try:
#             return vectorstore.as_retriever(
#                 search_kwargs={
#                     "k": self.config.retrieval_k
#                 }
#             )
#         except Exception as e:
#             print(f"Error creating fallback retriever: {e}")
#             raise RetrievalException("Failed to create fallback retriever") from e
#     def retrieve_with_fallback(self, vectorstore, question:str, file_type:str):
#         """"Retrieve documents with fallback logic"""
#         try:
#             # Filtered retrieval first
#             try:
#                 retriever = self.get_boosted_retriever(vectorstore, file_type)
#                 docs = retriever.get_relevant_documents(question)
#                 if docs:
#                     print(f"Retrieved {len(docs)} documents for file type '{file_type}'")
#                     return RetrievalResult(
#                         documents=docs,
#                         sources_count=len(docs),
#                         context=self._format_context(docs),
#                         retrieval_method="filtered",
#                     )
#                 else:
#                     print(f"No documents found for file type '{file_type}', using fallback")
#             except RetrievalException as e:
#                 print(f"Retrieval failed for file type '{file_type}': {e}")

#             # Fallback retrieval
#             fallback_retriever = self.get_fallback_retriever(vectorstore)
#             fallback_docs = fallback_retriever.get_relevant_documents(question)
#             if fallback_docs:
#                 print(f"Retrieved {len(fallback_docs)} documents using fallback retrieval")
#                 return RetrievalResult(
#                     documents=fallback_docs,
#                     sources_count=len(fallback_docs),
#                     retrieval_method="fallback",
#                     context=self._format_context(fallback_docs)
#                 )
#             else:
#                 print("No documents found in fallback retrieval")
#                 return RetrievalResult(
#                     documents=[],
#                     sources_count=0,
#                     retrieval_method="fallback",
#                 )
#         except Exception as e:
#             print(f"Error during document retrieval: {e}")
#             raise RetrievalException("Failed to retrieve documents: " + str(e)) from e
    
#     def _format_context(self, docs: List[Document]) -> str:
#         """"Format retrieved documents into a single context string"""
#         if not docs:
#             return "No relevant context found."
#         formatted_docs = []
#         for doc in docs:
#             file_type = doc.metadata.get('file_type', 'unknown')
#             content = doc.page_content.strip()
#             formatted_docs.append(f"[File Type: {file_type}]:\n{content}\n")
#         return "\n".join(formatted_docs)

# class ResponseGenerator:
#     def __init__(self, config:RAGConfig):
#         self.config = config
#         self.llm = ChatOpenAI(
#             model_name=self.config.llm_model,
#             temperature=self.config.generation_temp,
#             max_tokens=500
#         )
#         self.contextual_prompt = ChatPromptTemplate.from_template(
#             """
#             You are an intelligent personal assistant helping a user with questions about their life, work, health, and personal goals.

#             The context below comes from the user's personal documents, tagged with file types:
#             - work: Professional tasks, meetings, career-related content
#             - health: Fitness, nutrition, medical information, wellness
#             - personal: Family, friends, hobbies, daily life, social activities  
#             - reflection: Thoughts, emotions, self-analysis, mood tracking

#             If no relevant context is found, politely explain that you don't have enough information in their personal knowledge base to answer the question, and suggest they might want to add more relevant documents.

#             Context:
#             {context}

#             Question: {question}

#             Please provide a helpful, personalized answer based on the context above. If the context is insufficient, be honest about the limitations.

#             Answer:
#             """
#         )
    
#     def generate_response(self, question:str, context:str) -> str:
#         """"Generate a response based on the question and context"""
#         try:
#             inputs = {
#                 "question": question,
#                 "context": context
#             }

#             formatted_prompt = self.contextual_prompt.format(**inputs)
#             answer = self.llm.invoke(formatted_prompt)
#             if hasattr(answer, 'content'):
#                 content = answer.content
#             else:
#                 content = str(answer)
#             return content.strip()
            
#         except Exception as e:
#             print(f"Error generating response: {e}")
#             raise GenerationException("Failed to generate response: " + str(e)) from e

# class RAGService:
#     """Main RAG service that orchestrates the entire process"""
    
#     def __init__(self):
#         self.config = RAGConfig()
#         self.classifier = QuestionClassifier(self.config)
#         self.retriever = DocumentRetriever(self.config)
#         self.generator = ResponseGenerator(self.config)
        
#         # Cache for RAG chains and components
#         self.chain_cache: Dict[str, Tuple[Any, float]] = {}  # (chain, timestamp)
#         self.vectorstore_cache: Dict[str, Tuple[Any, float]] = {}  # (vectorstore, timestamp)
    
#     def _get_cached_vectorstore(self, user_id: str):
#         """Get cached vectorstore or create new one"""
#         if user_id in self.vectorstore_cache:
#             vectorstore, timestamp = self.vectorstore_cache[user_id]
#             if time.time() - timestamp < self.config.cache_ttl:
#                 return vectorstore
#             else:
#                 del self.vectorstore_cache[user_id]
        
#         # Create new vectorstore and cache it
#         vectorstore = get_user_vector_store(user_id)
#         if vectorstore is None:
#             raise RetrievalException(f"No vector store found for user {user_id}")
        
#         self.vectorstore_cache[user_id] = (vectorstore, time.time())
#         return vectorstore
    
#     async def process_question(self, question: str, user_id: str, request_id: str) -> Dict[str, Any]:
#         """Process a question through the complete RAG pipeline"""
#         try:
#             vectorstore = self._get_cached_vectorstore(user_id)
            
#             classification_result = self.classifier.classify_with_retry(question)
            
#             retrieval_result = self.retriever.retrieve_with_fallback(
#                 vectorstore, question, classification_result.category
#             )
            
#             answer = self.generator.generate_response(question, retrieval_result.context)
            
#             return {
#                 "answer": answer,
#                 "classification": classification_result.category,
#                 "context_sources": retrieval_result.sources_count,
#                 "metadata": {
#                     "classification_attempts": classification_result.attempts,
#                     "retrieval_method": retrieval_result.retrieval_method
#                 }
#             }
            
#         except (ClassificationException, RetrievalException, GenerationException):
#             # Re-raise specific exceptions
#             raise
#         except Exception as e:
#             # logger.error(f"Unexpected error in RAG processing: {str(e)}")
#             raise RAGException(f"RAG processing failed: {str(e)}")
    
#     def get_cache_stats(self) -> Dict[str, Any]:
#         """Get cache statistics"""
#         current_time = time.time()
        
#         # Count valid cache entries
#         valid_chains = sum(1 for _, timestamp in self.chain_cache.values() 
#                           if current_time - timestamp < self.config.cache_ttl)
#         valid_vectorstores = sum(1 for _, timestamp in self.vectorstore_cache.values() 
#                                 if current_time - timestamp < self.config.cache_ttl)
        
#         return {
#             "size": valid_chains + valid_vectorstores,
#             "chain_cache_size": valid_chains,
#             "vectorstore_cache_size": valid_vectorstores,
#             "total_entries": len(self.chain_cache) + len(self.vectorstore_cache)
#         }
    
#     def get_config_info(self) -> Dict[str, Any]:
#         """Get configuration information"""
#         return {
#             "retrieval_k": self.config.retrieval_k,
#             "max_question_length": self.config.max_question_length,
#             "cache_ttl": self.config.cache_ttl,
#             "classification_retries": self.config.classification_retries,
#             "llm_model": self.config.llm_model
#         }
    
#     def clear_user_cache(self, user_id: str) -> bool:
#         """Clear cache for a specific user"""
#         cleared = False
        
#         if user_id in self.chain_cache:
#             del self.chain_cache[user_id]
#             cleared = True
            
#         if user_id in self.vectorstore_cache:
#             del self.vectorstore_cache[user_id]
#             cleared = True
            
#         return cleared
    
#     def clear_all_cache(self) -> int:
#         """Clear all caches"""
#         total_count = len(self.chain_cache) + len(self.vectorstore_cache)
#         self.chain_cache.clear()
#         self.vectorstore_cache.clear()
#         return total_count
    
#     def cleanup_expired_cache(self):
#         """Remove expired cache entries"""
#         current_time = time.time()
        
#         # Clean up chain cache
#         expired_chains = [user_id for user_id, (_, timestamp) in self.chain_cache.items()
#                          if current_time - timestamp >= self.config.cache_ttl]
#         for user_id in expired_chains:
#             del self.chain_cache[user_id]
        
#         # Clean up vectorstore cache
#         expired_vectorstores = [user_id for user_id, (_, timestamp) in self.vectorstore_cache.items()
#                                if current_time - timestamp >= self.config.cache_ttl]
#         for user_id in expired_vectorstores:
#             del self.vectorstore_cache[user_id]
        
#         if expired_chains or expired_vectorstores:
#             print(f"Cleaned up {len(expired_chains)} chain cache entries and "
#                        f"{len(expired_vectorstores)} vectorstore cache entries")

# Classification prompt
# classification_prompt = PromptTemplate.from_template(
#             """
#             Classify the following user question into EXACTLY ONE of these categories: work, health, personal, reflection
            
#             Guidelines:
#             - work: Job tasks, meetings, deadlines, career, professional development
#             - health: Exercise, nutrition, medical, fitness, sports, wellness
#             - personal: Family, friends, home, hobbies, social activities, daily tasks
#             - reflection: Emotions, thoughts, self-analysis, mood, feelings, introspection
            
#             Question: {question}
            
#             Respond with ONLY the category name (work/health/personal/reflection):
#             """
#         )

# classification_chain = (
#     classification_prompt
#     | ChatOpenAI(temperature=0)
#     | StrOutputParser()
# )

# # Retrieval logic (depends on classification)
# def retrieve_context(inputs):
#     classification = inputs["classification"]
#     user_id = inputs["user_id"]
#     question = inputs["question"]

#     try:
#         vectorstore = get_user_vector_store(user_id)
#         retriever = vectorstore.as_retriever(search_kwargs={
#             "k": 5,
#             "filter": {"file_type": classification}
#         })
#         docs = retriever.invoke(question)
#         context = "\n\n".join(doc.page_content for doc in docs)
#     except Exception as e:
#         raise RetrievalException(str(e))

#     return {
#         "context": context,
#         "documents": docs,
#         "classification": classification,
#         "question": question
#     }


# # Generation prompt
# generation_prompt = ChatPromptTemplate.from_template(
#             """
#             You are an intelligent personal assistant helping a user with questions about their life, work, health, and personal goals.

#             The context below comes from the user's personal documents, tagged with file types:
#             - work: Professional tasks, meetings, career-related content
#             - health: Fitness, nutrition, medical information, wellness
#             - personal: Family, friends, hobbies, daily life, social activities  
#             - reflection: Thoughts, emotions, self-analysis, mood tracking

#             If no relevant context is found, politely explain that you don't have enough information in their personal knowledge base to answer the question, and suggest they might want to add more relevant documents.

#             Context:
#             {context}

#             Question: {question}

#             Please provide a helpful, personalized answer based on the context above. If the context is insufficient, be honest about the limitations.

#             Answer:
#             """
#         )
    

# llm = ChatOpenAI(model="gpt-4", temperature=0.1, streaming=True)

# generation_chain = generation_prompt | llm


# # Step: Run generation, return streaming + metadata
# def generate_with_metadata(inputs):
#     prompt_input = {
#         "context": inputs["context"],
#         "question": inputs["question"]
#     }

#     # We'll return a generator for streaming
#     async def stream_gen():
#         async for chunk in generation_chain.astream(prompt_input):
#             yield chunk.content or ""

#     return {
#         "stream": stream_gen(),
#         "file_type": inputs["classification"],
#         "num_sources": len(inputs["documents"]),
#         "source_chunks": [
#             {
#                 "content": doc.page_content,
#                 "metadata": doc.metadata
#             } for doc in inputs["documents"]
#         ]
#     }

# rag_chain = (
#     RunnableMap({
#         "question": lambda x: x["question"],
#         "user_id": lambda x: x["user_id"],
#         "classification": RunnableLambda(lambda x: classification_chain.ainvoke(x["question"]))
#     })
#     | RunnableLambda(retrieve_context)
#     | RunnableLambda(generate_with_metadata)
# )

