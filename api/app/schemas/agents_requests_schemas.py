from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.schemas.chat_schemas import ChatRequest
import uuid

class OrchestratorData(BaseModel):
	manager_name : str = Field(description="Manager's name", min_length=1)
	manager_email: EmailStr = Field(description="Manager's email")
	user_name: str = Field(description="User's name", min_length=1)
	user_email: EmailStr = Field(description="User's email")
	ticket_id: uuid.UUID = Field(description="Ticket's id")
	created_at: datetime = Field(description="Date of ticket creation")
	user_message: str = Field(description="User's message to the orchestrator", min_length=1)

class OrchestratorResponse(BaseModel):
	ticket_id: uuid.UUID = Field(description="Ticket's id")
	orchestrator_message: str = Field(description="Orchestrator's message to the user", min_length=1)