from pydantic import BaseModel

class chatbot_api(BaseModel):
    user_query: str