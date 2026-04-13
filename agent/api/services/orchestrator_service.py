from api.schemas.agents_requests_schemas import OrchestratorRequest
from app.agents.agent_request.agent_initial_request import call_orchestrator_agent
from openai import OpenAI
import os

def sanitize_output_message(response: dict):
	new_input = {}

	for item in response:
		if item.type == "message":
			orchestrator_message = item.content[0].text

			new_input = {
				"role" : "assistant",
				"content" : orchestrator_message
			}

	return new_input

def send_request_to_orchestrator(req: OrchestratorRequest):
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
			"id": "#4821",
			"reason": "Need approvisionnement",
			"created_at": "08/04/2026"
		}
	}
	req_input_list = [{"role": "user", "content": "Can I get a new keyboard ?"}]


	response = call_orchestrator_agent(client, data, req_input_list)
	# input_to_append = sanitize_output_message(response)
	# print(input_to_append)
	# Ici je dois faire un return array dans la fct de l'orchestrator qui va me permettre d'avoir tout l'input list qui s'append petit a petit. Ex apres un tool_call append puis apres j'
	# j'append le msg de l'assistant. reteste le code tu verras

	return (0)