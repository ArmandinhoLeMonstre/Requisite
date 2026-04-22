from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.ticket import TicketStatus
import uuid


class TicketBase(BaseModel):
	status: TicketStatus
	description: str
	user_id: int


class RequestTicket(TicketBase):
	pass


class ResponseTicket(TicketBase):
	model_config = ConfigDict(from_attributes=True)
	
	id: uuid.UUID
	created_at: datetime