from pydantic import BaseModel

class chatbot_api(BaseModel):
    userId: str
    user_query: str
    
    
class langchain_eval_qa_api(BaseModel):
    userId: str
    question: list
    ref_answer: list