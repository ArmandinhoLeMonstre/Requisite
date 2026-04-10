from pydantic import BaseModel, Field

class OrchestratorRequest(BaseModel):
	user_id: int = Field(gt=0)
	user_message: str = Field(description="User's message to the orchestrator", min_length=1)