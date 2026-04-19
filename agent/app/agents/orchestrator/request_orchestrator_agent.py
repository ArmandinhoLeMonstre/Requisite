from openai import OpenAI, OpenAIError
from app.agents_exceptions import OrchestratorError
import json
from json import JSONDecodeError
from app.tools.request_tools.registry import TOOL_REGISTRY
from app.tools.request_tools.definitions import TOOLS
from app.agents.orchestrator.prompt_orchestrator import get_orchestrator_prompt

def call_orchestrator_agent(client: OpenAI, data: dict, req_input_list: list):

	return_reponse = []

	input_list = [
		{
			"role": "system",
			"content": f"""Here is the current request context. Use this data when calling the email_agent.
			Always pass the complete and updated data to the email_agent when calling it.
			
			{json.dumps(data, indent=2)}
			"""
		},
	]

	if req_input_list is not None:
		input_list.extend(req_input_list)

	prompt = get_orchestrator_prompt(data)

	while True:
		try:
			response = client.responses.create(
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

		for item in response.output:
			if item.type == "message":
				print(f"Assistant: {item.content[0].text}")
				return_reponse.append(response.output)
				return {
					"message": item.content[0].text,
					"input_list": return_reponse
				}

			elif item.type == "function_call":
				return_reponse.append(response.output)
				func = TOOL_REGISTRY.get(item.name)
				if not func:
					raise OrchestratorError(message="The orchestrator tried to call a tool that is not available in the registry.")
				try:
					parsed = json.loads(item.arguments)
				except JSONDecodeError as e:
					raise OrchestratorError(message=f"Failed to parse tool arguments as JSON: {e}. Raw arguments: {item.arguments}")
					# log -> print (f"Couldn't load arguments for function_call correctly : {e}")
				try:
					tool_result = func(**parsed)
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