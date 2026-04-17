from api.schemas.agents_requests_schemas import OrchestratorRequest
from app.agents.agent_request.agent_initial_request import call_orchestrator_agent
from openai import OpenAI
import api.services.formatter_service as formatter_service
import os
import json


def send_request_to_orchestrator(req: OrchestratorRequest, existing_input_list: list):
	openai_api_key = os.getenv("OPENAI_API_KEY")

	client = OpenAI(
		api_key=openai_api_key
	)

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

	orchestrator_response = call_orchestrator_agent(client, data, req_input_list)

	new_input = formatter_service.format_orchestrator_message(orchestrator_response)
	req_input_list.extend(new_input)

	return (json.dumps(req_input_list))