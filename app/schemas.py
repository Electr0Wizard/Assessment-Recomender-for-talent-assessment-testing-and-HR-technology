from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Message(BaseModel):
    role: str # "user", "assistant", or "system"
    content: str

class AssessmentRecommendation(BaseModel):
    name: str
    url: HttpUrl
    test_type: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str
    recommendations: Optional[List[AssessmentRecommendation]] = None
    end_of_conversation: bool