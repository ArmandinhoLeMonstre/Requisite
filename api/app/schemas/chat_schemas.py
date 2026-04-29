from pydantic import BaseModel
from app.models.chat_model import Sender


class ChatBase(BaseModel):
	sender: Sender
	message: str

class ChatRequest(ChatBase):
	pass

class ChatResponse(ChatBase):
	pass
