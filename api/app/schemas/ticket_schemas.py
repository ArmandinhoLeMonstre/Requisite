from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.ticket_model import TicketStatus
from app.schemas.chat_schemas import ChatResponse
import uuid


class TicketBase(BaseModel):
	pass


class TicketCreate(TicketBase):
	user_message: str


class TicketResponse(TicketBase):
	model_config = ConfigDict(from_attributes=True)
	
	status: TicketStatus | None = None
	description: str | None = Field(min_length=1, max_length=200)
	user_id: int
	id: uuid.UUID
	user_name: str | None = None
	created_at: datetime


class TicketChats(TicketBase):
	id: uuid.UUID
	user_id: int
	chats: list[ChatResponse]


class TicketsGroup(TicketBase):
	model_config = ConfigDict(from_attributes=True)

	chats: dict[str,list[TicketResponse]]
