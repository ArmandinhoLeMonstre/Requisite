from app.schemas.agents_requests_schemas import OrchestratorRequest
from app.agents_app.agents.orchestrator.request_orchestrator_agent import call_orchestrator_agent
from app.agents_app.agents_exceptions import OrchestratorError
from fastapi import HTTPException, status
from openai import OpenAI
import app.services.formatter_service as formatter_service
import os
import json

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
	api_key=openai_api_key
)

def send_request_to_orchestrator(req: OrchestratorRequest, existing_input_list: list):

	data = {
		"employee": {
			"name": "Ricardo",
			"department": "Marketing",
			"email": "rafael.nascimento@outlook.be"
		},
		"manager": {
			"name": "Armand",
			"email": "armandeuarmand@gmail.com"
		},
		"ticket": {
			"id": "#6242",
			"reason": "Need approvisionnement",
			"created_at": "08/04/2026"
		}
	}
	req_input_list = []
	if existing_input_list:
		req_input_list.extend(existing_input_list)

	req_input_list.extend([{"role": "user", "content": req.user_message}])

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