from openai import AsyncOpenAI
import os
import json
from json import JSONDecodeError
from app.agents_app.tools.inventory_tools.check_inventory import check_inventory
from app.agents_app.tools.inventory_tools.registry import TOOL_REGISTRY
from app.agents_app.tools.inventory_tools.definitions import TOOLS

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)

async def call_inventory_agent(object_type: str, object_specs: str):
	if not object_type:
		return {
			"success": False,
			"error_code": "MISSING_ARGUMENT",
			"field": "object_type",
			"message": "The object type is required to check the inventory.",
			"action": "Ask the user what type of object they want to acquire."
		}
	if not object_specs:
		return {
			"success": False,
			"error_code": "MISSING_ARGUMENT",
			"field": "object_specs",
			"message": "The object specs are required to check the inventory",
			"action": "Ask the user what type of specs the object has."
		}

	input_list = [
		{"role": "user", "content": f"Check the inventory for: {object_type}"}
	]

	try:
		response = await client.responses.create(
			model="gpt-4o-mini",
			instructions="""You are an inventory checker agent.

			## Your only job:
			Call the check_inventory tool with the object type provided by the user.

			## After getting the result:
			- If objects are found: return them as a JSON array
			- If nothing is found: return an empty array []
			- Never make up results — only return what the tool gives you

			## Output format (always):
			{"found": true/false, "items": [...]}
			""",
			tools=TOOLS,
			input=input_list
		)
	except Exception as e:
		# ici il faut log print({"error" : f"an error has occured while making a request to the LLM API : {e}"})
		return {
			"success": False,
			"error_code": "API_ERROR",
			"message": "API call to openAI failed"
		}

	input_list += response.output

	for item in response.output:
		if item.type == "function_call":
			func = TOOL_REGISTRY.get(item.name)

			if not func:
				return {
				"success": False,
				"error_code": "TOOL_NOT_FOUND",
				"message": f"Tool '{item.name}' not found in registry.",
				"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
			}

			try:
				parsed = json.loads(item.arguments)
			except JSONDecodeError as e:
				# log -> print (f"Couldn't load arguments for function_call correctly : {e}")
				return {
					"success": False,
					"message": "Couldn't load arguments for function_call correctly",
					"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
				}

			try:
				tool_result = func(**parsed) #ici ya un pb si le tool ne renvoie pas d'erreurs si les params sont pas bien envoyes
			except Exception as e:
				# log -> print({"error": f"tool {item.name} has raised an error : {e}"})
				return {
					"success": False,
					"message": "An error has been raised during a tool_call",
					"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
				}

			input_list.append({
				"type": "function_call_output",
				"call_id": item.call_id,
				"output": json.dumps(tool_result)
			})

			input_list.append({
				"role": "user",
				"content": f"""The user is looking for a {object_type} with these specs: {object_specs}.
				Rank the items above from best to worst match based on the specs.
				Return ONLY a raw JSON array, no markdown, no backticks, no preamble..
				Add a 'match_score' (0-10) and 'match_reason' field to each item."""
			})

			try:
				ranked_response = await client.responses.create(
					model="gpt-4o-mini",
					instructions="You are an inventory ranking agent. Rank products by how well they match the user's specs. Never invent specs that are not in the item data.",
					input=input_list
				)
			except Exception as e:
				# log -> print({"error" : f"an error has occured while making a request to the LLM API : {e}"})
				return {
					"success": False,
					"error_code": "API_ERROR",
					"message": "API call to openAI failed"
				}

			try:
				ranked_text = ranked_response.output[0].content[0].text
			except (IndexError, AttributeError) as e:
				# log -> print(f"Unexpected response structure: {e}")
				return {
					"success": False,
					"message": "Unexpected response structure",
					"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
				}
			
			return {
				"success": True,
				"data": ranked_text
			}