from pydantic import BaseModel, Field

class OrchestratorRequest(BaseModel):
	ticket_id: int = Field(gt=0)
	user_message: str = Field(description="User's message to the orchestrator", min_length=1)

class OrchestratorResponse(BaseModel):
	ticket_id: int = Field(gt=0)
	orchestrator_message: str = Field(description="Orchestrator's message to the user", min_length=1)