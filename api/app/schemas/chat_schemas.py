from pydantic import BaseModel
from app.models.chat import Sender


class ChatBase(BaseModel):
	sender: Sender
	message: str

class ChatRequest(ChatBase):
	pass

class ChatResponse(ChatBase):
	pass
