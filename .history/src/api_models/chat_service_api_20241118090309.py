from pydantic import BaseModel

class chatbot_api(BaseModel):
    userId: str
    user_query: str