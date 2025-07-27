from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser


class ResponseGenerator:
    def __init__(self, model_name:str, temperature:float, generation_prompt:str):
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            streaming=True
        )
        self.contextual_prompt = ChatPromptTemplate.from_template(generation_prompt)

    def as_runnable(self):
            return self.contextual_prompt | self.llm | StrOutputParser()