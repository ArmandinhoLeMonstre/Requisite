from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.agents_requests_schemas import OrchestratorRequest
import api.services.orchestrator_service as orchestrator_service
import api.services.db_service as db_service
from typing import Annotated
from api.database import get_db

router = APIRouter(prefix="/agents")

@router.post("/")
def call_agents_orchestrator(req: OrchestratorRequest, db: Annotated[Session, Depends(get_db)]):
	existing_input_list = db_service.retrieve_input_list(db, req.ticket_id)
	result = orchestrator_service.send_request_to_orchestrator(req, existing_input_list)
	db_service.save_input_list(db, req.ticket_id, result.get("history"))
	return {"message": result.get("message")}