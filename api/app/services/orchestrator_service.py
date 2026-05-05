from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from app.models.user_model import User
from app.models.ticket_model import Ticket
from app.schemas.agents_requests_schemas import OrchestratorResponse
from app.schemas.agents_requests_schemas import OrchestratorData
from app.agents_app.agents.orchestrator_agent import call_orchestrator_agent
from app.agents_app.agents_exceptions import OrchestratorError
from fastapi import HTTPException, status
from openai import OpenAI
import app.services.db_service as db_service
import app.services.formatter_service as formatter_service
import os
import json
from app.logger import logger

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
	api_key=openai_api_key
)

def send_request_to_orchestrator(message: str, existing_input_list: list, data: OrchestratorData):

	req_input_list = []
	if existing_input_list:
		req_input_list.extend(existing_input_list)

	req_input_list.extend([{"role": "user", "content": message}])

	try:
		orchestrator_response = call_orchestrator_agent(client, data, req_input_list)
	except OrchestratorError as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

	new_input = formatter_service.format_orchestrator_message(orchestrator_response.get("input_list"))
	req_input_list.extend(new_input)

	updated_input_list = json.dumps(req_input_list)

	return ({
		"history": updated_input_list,
		"message": orchestrator_response.get("message")
	})


def create_data(current_user: User, db : Session, ticket: Ticket, msg: str):
	try:
		manager = db.scalars(select(User).where(User.id == current_user.group.manager_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="Manager not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	data = OrchestratorData(
		manager_name= manager.name,
		manager_email= manager.email,
		user_name= current_user.name,
		user_email= current_user.email,
		ticket_id= ticket.id,
		created_at= ticket.created_at,
		user_message= msg
	)

	return data


def call_agents_orchestrator(data: OrchestratorData, db: Session, message: str):
	existing_input_list = db_service.retrieve_input_list(db, data.ticket_id)

	result = send_request_to_orchestrator(message, existing_input_list, data)

	db_service.save_input_list(db, data.ticket_id, result.get("history"))

	response = OrchestratorResponse(
		ticket_id=data.ticket_id,
		orchestrator_message=result.get("message")
	)

	return (response)