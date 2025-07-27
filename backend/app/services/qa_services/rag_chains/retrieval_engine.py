from langchain_core.runnables import RunnableMap, RunnableLambda, RunnablePassthrough
from app.schemas.qa_schema import RetrievalResult

class RetrievalEngine:
    def __init__(self, vectorstore, k:int, allow_fallback:bool=True):
        self.vectorstore = vectorstore
        self.retrieval_k = k
        self.allow_fallback = allow_fallback

    def as_runnable(self):
            def retrieve(inputs) -> RetrievalResult: 
                question = inputs["question"]
                classification = inputs.get("classification", "personal")
                retriever = self.vectorstore.as_retriever(
                    search_kwargs={
                        "k": self.retrieval_k,
                        "filter": {"file_type": classification},
                    }
                )
                docs = retriever.get_relevant_documents(question)

                if not docs and self.allow_fallback:
                    fallback_retriever = self.vectorstore.as_retriever(
                        search_kwargs={
                            "k": self.retrieval_k,
                        }
                    )
                    docs = fallback_retriever.get_relevant_documents(question)

                context = "\n\n".join([
                    f"[File Type: {doc.metadata.get('file_type', 'unknown')}]:\n{doc.page_content}"
                    for doc in docs
                ]) if docs else "No relevant documents found in your personal knowledge base."


                return {
                    "context": context,
                    "question": question,
                    "classification": classification,
                    "sources_count": len(docs)
                }

            return RunnableLambda(retrieve)
