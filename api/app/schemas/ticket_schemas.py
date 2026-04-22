from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.ticket import TicketStatus
from app.schemas.user_schemas import ResponseUser
import uuid


class TicketBase(BaseModel):
	status: TicketStatus
	description: str = Field(min_length=1, max_length=200)
	user_id: int


class RequestTicket(TicketBase):
	pass


class ResponseTicket(TicketBase):
	model_config = ConfigDict(from_attributes=True)
	
	id: uuid.UUID
	created_at: datetime
	# user: ResponseUser TODO