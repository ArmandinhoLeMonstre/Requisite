from openai import AsyncOpenAI, OpenAIError
from app.agents_app.agents_exceptions import OrchestratorError
import json
from json import JSONDecodeError
from app.agents_app.tools.request_tools.registry import TOOL_REGISTRY
from app.agents_app.tools.request_tools.definitions import TOOLS
from app.agents_app.agents.orchestrator_prompt import get_orchestrator_prompt
from app.schemas.agents_requests_schemas import OrchestratorData

from app.logger import logger

async def call_orchestrator_agent(client: AsyncOpenAI, data: OrchestratorData, req_input_list: list):
	log = logger.bind(ticket_id=data.ticket_id)
	orchestrator_log = log.bind(agent="orchestrator")

	orchestrator_log.info("orchestrator.started")

	return_reponse = []

	input_list = [
		{
			"role": "system",
			"content": f"""Here is the current request context. Use this data when calling the email_agent.
			Always pass the complete and updated data to the email_agent when calling it.
			
			{json.dumps(data.model_dump(mode='json'), indent=2)}
			"""
		},
	]

	if req_input_list is not None:
		input_list.extend(req_input_list)

	prompt = get_orchestrator_prompt(data)

	while True:
		try:
			response = await client.responses.create(
				model="gpt-4o-mini",
				instructions = prompt,
				tools=TOOLS,
				input=input_list
			)
		except OpenAIError as e:
			raise OrchestratorError(message=str(e))
		except Exception as e:
			raise OrchestratorError(message=str(e))
		input_list += response.output

		return_flag = True

		for item in response.output:
			if item.type == "message":
				print(f"Assistant: {item.content[0].text}")
				return_reponse.append([item])

			elif item.type == "function_call":
				return_flag = False
				return_reponse.append([item])
				func = TOOL_REGISTRY.get(item.name)
				if not func:
					orchestrator_log.error(
						"orchestrator.func_error",
						error=str(e),
						raw_arguments=item.name
					)
					raise OrchestratorError(message="The orchestrator tried to call a tool that is not available in the registry.")
				orchestrator_log.info("orchestrator.tool_called", tool_name=item.name)
				try:
					parsed = json.loads(item.arguments)
				except JSONDecodeError as e:
					orchestrator_log.error(
						"orchestrator.parse_error",
						error=str(e),
						raw_arguments=item.arguments
					)
					raise OrchestratorError(message=f"Failed to parse tool arguments as JSON: {e}. Raw arguments: {item.arguments}")
				try:
					tool_result = await func(**parsed)
					
					success = tool_result.get("success")
					if success is False:
						print("false")
						# ici, je veux log ppurquoi  success false, donc refractor tous les retuns d'agents
						# pour log l'erreur exacte. Donc avoir msg + action
				except Exception as e:
					#Ici, il y a un pb, faudra regler et revisiter les json d'erreur des agents etc...
					print(f"Error in tool : {e}")
					# log -> print({"error": f"tool {item.name} has raised an error : {e}"})
					# return {
					# 	"success": False,
					# 	"message": "An error has been raised during a tool_call",
					# 	"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
					# }
				return_reponse.append([{
					"type": "function_call_output",
					"call_id": item.call_id,
					"output": json.dumps(tool_result)
				}])
				input_list.append({
					"type": "function_call_output",
					"call_id": item.call_id,
					"output": json.dumps(tool_result)
				})
		if return_flag is True:
			orchestrator_log.info("orchestrator.completed")
			return {
					"message": item.content[0].text,
					"input_list": return_reponse
				}