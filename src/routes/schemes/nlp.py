from pydantic import BaseModel
from typing import Optional, List

class Message(BaseModel):
    role: str
    content: str

class PushRequest(BaseModel):

    do_reset : Optional[int] = 0


class SearchRequest(BaseModel):
    text : str
    limit: Optional[int] = 5
    chat_history: Optional[List[Message]] = []
    language_instruction: Optional[str] = None
    session_id: Optional[str] = None