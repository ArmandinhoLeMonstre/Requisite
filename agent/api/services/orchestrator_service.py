from api.schemas.agents_requests_schemas import OrchestratorRequest
from app.agents.agent_request.agent_initial_request import call_orchestrator_agent
from openai import OpenAI
import os

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

	call_orchestrator_agent(client, data)
	return (0)