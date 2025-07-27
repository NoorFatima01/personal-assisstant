from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import StrOutputParser


class QuestionClassifier:
    def __init__(self, model_name:str, temperature:float, prompt_template:str):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature
        )
        self.classification_prompt = PromptTemplate.from_template(prompt_template)

        self.chain = self.classification_prompt | self.llm | StrOutputParser()

    def as_runnable(self):
            return self.chain
