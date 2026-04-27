from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.ticket import TicketStatus
from app.schemas.chat_schemas import ChatResponse
import uuid


class TicketBase(BaseModel):
	pass


class TicketCreate(TicketBase):
	message: str


class TicketResponse(TicketBase):
	model_config = ConfigDict(from_attributes=True)
	
	status: TicketStatus
	description: str | None = Field(min_length=1, max_length=200)
	user_id: int
	id: uuid.UUID
	chats: list[ChatResponse]
	created_at: datetime
