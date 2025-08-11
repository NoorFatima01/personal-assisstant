from langchain_core.runnables import RunnableLambda
from app.utils.qa_utils import create_search_filter
from typing import List

class RetrievalEngine:
    def __init__(self, vectorstore, k: int, allow_fallback: bool = True):
        self.vectorstore = vectorstore
        self.retrieval_k = k
        self.allow_fallback = allow_fallback

    def as_runnable(self):
        def retrieve(inputs):            
            try:
                question: str = inputs["question"]
                week_start: List[str] = inputs.get("week_start", None) # will be an array
                classification: List[str] = inputs.get("classification", ["personal"]) # will be an array

                filter = create_search_filter(classification, week_start)

                retriever = self.vectorstore.as_retriever(
                    search_kwargs={
                        "k": self.retrieval_k,
                        "filter": filter,
                    }
                )


                docs = retriever.invoke(question)
                
                if not docs and self.allow_fallback:
                    fallback_retriever = self.vectorstore.as_retriever(
                        search_kwargs={"k": self.retrieval_k}
                    )
                    docs = fallback_retriever.invoke(question)
                
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

                return result

            except Exception as e:
                import traceback
                traceback.print_exc()
                raise

        return RunnableLambda(retrieve)