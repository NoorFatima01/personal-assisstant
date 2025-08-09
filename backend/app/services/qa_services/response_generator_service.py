from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_core.runnables import RunnableLambda
from app.services.chat_services.chat_db_service import ChatDBService

# gets question, classification, context, source count as input but only uses question and context
class ResponseGenerator:
    def __init__(self, llm, generation_prompt: str, chat_service: ChatDBService, user_id: str, chat_id: str):
        self.llm = llm
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(generation_prompt),  # The system-level instruction
            HumanMessagePromptTemplate.from_template("Please help me with this question: {question}") 
        ])
        self.user_id = user_id
        self.chat_id = chat_id
        self.chat_service = chat_service

    def _generate_response(self, inputs):
        try:
            question = inputs["question"]
            context = inputs["context"]

            chat_history = self.chat_service.get_or_create_chat_session(self.chat_id, self.user_id).get("messages", [])
            # Format chat history (you may need to adjust based on your prompt)
            formatted_history = "\n".join(
                [f"User: {msg['user_input']}\nAssistant: {msg['assistant_response']}" for msg in chat_history[-10:]]
            )

            # Proper chain
            chain = self.prompt_template | self.llm | StrOutputParser()

            response = chain.invoke({
                "question": question,
                "context": context,
                "chat_history": formatted_history
            })

            # Save the response to the chat history
            self.chat_service.update_chat_session(self.chat_id, [{"user_input": question, "assistant_response": response}])
            return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, something went wrong while generating the response."

    def as_runnable(self):
        return RunnableLambda(self._generate_response)