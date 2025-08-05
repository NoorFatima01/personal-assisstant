from langchain_core.runnables import RunnableMap, RunnableLambda, RunnablePassthrough
from app.schemas.qa_schema import RetrievalResult

class RetrievalEngine:
    def __init__(self, vectorstore, k: int, allow_fallback: bool = True):
        self.vectorstore = vectorstore
        self.retrieval_k = k
        self.allow_fallback = allow_fallback

    def as_runnable(self):
        def retrieve(inputs):
            print(f"=== RETRIEVAL DEBUG ===")
            
            try:
                question = inputs["question"]
                week_start = inputs.get("week_start", None)
                classification = inputs.get("classification", "personal")
                
                # Handle empty classification
                if not classification or classification.strip() == "":
                    print("Warning: Empty classification, defaulting to 'personal'")
                    classification = "personal"
                filter = {
                    "must": [
                        {"key": "file_type", "match": {"value": classification}}
                    ]
                }

                if isinstance(week_start, list) and len(week_start) > 0:
                    # Add multiple week_start values using a "should" clause
                    week_start_conditions = [
                        {"key": "week_start", "match": {"value": week}} for week in week_start
                    ]
                    filter["must"].append({"should": week_start_conditions})

                retriever = self.vectorstore.as_retriever(
                    search_kwargs={
                        "k": self.retrieval_k,
                        # "filter": filter,
                    }
                )


                print(f"Created retriever with filter: {{'file_type': '{classification}', 'weekStart': '{week_start}'}}")

                docs = retriever.invoke(question)
                print(f"Retrieved {len(docs)} documents")
                
                if not docs and self.allow_fallback:
                    print("No docs found, trying fallback without filter")
                    fallback_retriever = self.vectorstore.as_retriever(
                        search_kwargs={"k": self.retrieval_k}
                    )
                    docs = fallback_retriever.invoke(question)
                    print(f"Fallback retrieved {len(docs)} documents")
                
                context = "\n\n".join([
                    f"[File Type: {doc.metadata.get('file_type', 'unknown')}]:\n{doc.page_content}"
                    for doc in docs
                ]) if docs else "No relevant documents found in your personal knowledge base."
                
                result = {
                    "context": context,
                    "question": question,
                    "classification": classification,
                    "sources_count": len(docs)
                }
                
                print(f"Retrieval result keys: {list(result.keys())}")
                print(f"Context length: {len(context)}")
                print(f"=== END RETRIEVAL DEBUG ===")
                
                return result
                
            except Exception as e:
                print(f"Retrieval error: {str(e)}")
                print(f"Exception type: {type(e)}")
                import traceback
                traceback.print_exc()
                raise

        return RunnableLambda(retrieve)