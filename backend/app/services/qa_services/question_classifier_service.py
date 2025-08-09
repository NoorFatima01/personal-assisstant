from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class QuestionClassifier:
    def __init__(self, llm, prompt_template: str):
        self.llm = llm
        self.classification_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_template),  # The system-level instruction
            HumanMessagePromptTemplate.from_template("Please help me classify this question: {question}") 
        ])
        self.chain = self.classification_prompt | self.llm | StrOutputParser()

    def _classify(self, question):
        """Debug wrapper for classification"""

        try:
            # Get LLM response
            llm_response = self.chain.invoke({"question": question})

            # validate the result
            valid_cats = ["work", "health", "personal", "reflection"]
            cleaned_response = llm_response.content.strip() if hasattr(llm_response, 'content') else str(llm_response).strip()

            if cleaned_response not in valid_cats and cleaned_response.lower() not in valid_cats:
                cleaned_response = "personal"

            return cleaned_response

        except Exception as e:
            print(f"Classification error: {str(e)}")
            print(f"Exception type: {type(e)}")
            return "personal"  # fallback

    def as_runnable(self):
        return RunnableLambda(self._classify)
