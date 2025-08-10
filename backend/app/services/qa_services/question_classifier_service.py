import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from typing import List


class QuestionClassifier:
    def __init__(self, llm, prompt_template: str):
        self.llm = llm
        self.classification_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(prompt_template),  # The system-level instruction
            HumanMessagePromptTemplate.from_template("Please help me classify this question: {question}") 
        ])
        self.chain = self.classification_prompt | self.llm | StrOutputParser()

    def _parse_categories(self, response_text: str) -> List[str]:
        """Parse categories from LLM response, handling various formats"""
        valid_cats = ["work", "health", "personal", "reflection"]
        
        try:
            # First, try direct JSON parsing
            categories = json.loads(response_text)
            if isinstance(categories, list):
                # Validate and filter categories
                valid_categories = [cat.lower().strip() for cat in categories if cat.lower().strip() in valid_cats]
                return valid_categories if valid_categories else ["personal"]
        except json.JSONDecodeError:
            pass
        
        try:
            # Single category fallback
            cleaned = response_text.lower().strip().strip('"\'')
            if cleaned in valid_cats:
                return [cleaned]
                
        except Exception as e:
            print(f"Parsing error: {e}")
        
        # Ultimate fallback
        return ["personal"]

    def _classify(self, question: str) -> List[str]:
        """Classify question and return array of categories"""
        try:
            # Get LLM response
            llm_response = self.chain.invoke({"question": question})
            
            # Extract text content
            response_text = llm_response.content.strip() if hasattr(llm_response, 'content') else str(llm_response).strip()
            
            # Parse categories
            categories = self._parse_categories(response_text)
            
            return categories

        except Exception as e:
            print(f"Classification error: {str(e)}")
            print(f"Exception type: {type(e)}")
            return ["personal"]  # fallback

    def as_runnable(self):
        return RunnableLambda(self._classify)






            # # Look for array-like patterns: ["work", "health"] or ['work', 'health']
            # array_match = re.search(r'\[(.*?)\]', response_text)
            # if array_match:
            #     content = array_match.group(1)
            #     # Extract quoted strings
            #     categories = re.findall(r'["\']([^"\']+)["\']', content)
            #     if categories:
            #         valid_categories = [cat.lower().strip() for cat in categories if cat.lower().strip() in valid_cats]
            #         return valid_categories if valid_categories else ["personal"]
            
            # # Look for comma-separated values without brackets
            # if ',' in response_text:
            #     categories = [cat.strip().strip('"\'') for cat in response_text.split(',')]
            #     valid_categories = [cat.lower().strip() for cat in categories if cat.lower().strip() in valid_cats]
            #     if valid_categories:
            #         return valid_categorie