from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.ticket import TicketStatus
import uuid


class TicketBase(BaseModel):
	status: TicketStatus
	description: str = Field(min_length=1, max_length=200)
	user_id: int


class TicketCreate(TicketBase):
	pass


class TicketResponse(TicketBase):
	model_config = ConfigDict(from_attributes=True)
	
	id: uuid.UUID
	created_at: datetime
