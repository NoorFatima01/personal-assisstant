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
            # Format the prompt first to see what's being sent
            # formatted_messages = self.classification_prompt.format_messages({"question": question})

            # Get LLM response
            llm_response = self.chain.invoke({"question": question})

            # validate the result
            valid_cats = ["work", "health", "personal", "reflection"]
            cleaned_response = llm_response.content.strip() if hasattr(llm_response, 'content') else str(llm_response).strip()

            if cleaned_response not in valid_cats and cleaned_response.lower() not in valid_cats:
                print(f"Invalid classification '{cleaned_response}', defaulting to 'personal'")
                cleaned_response = "personal"

            return cleaned_response

        except Exception as e:
            print(f"Classification error: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            return "personal"  # fallback

    def as_runnable(self):
        print("Creating QuestionClassifier runnable")
        return RunnableLambda(self._classify)
