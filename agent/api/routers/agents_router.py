from fastapi import APIRouter
from api.schemas.agents_requests_schemas import OrchestratorRequest
import api.services.orchestrator_service as orchestrator_service

router = APIRouter(prefix="/agents")

@router.post("/")
def call_agents_orchestrator(orchestrator_request: OrchestratorRequest):
	orchestrator_service.send_request_to_orchestrator(orchestrator_request)
	return {"Hello": "World"}