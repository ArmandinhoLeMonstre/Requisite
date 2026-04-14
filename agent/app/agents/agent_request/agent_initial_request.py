from openai import OpenAI
import os
import json
from json import JSONDecodeError
from app.tools.request_tools.registry import TOOL_REGISTRY
from app.tools.request_tools.definitions import TOOLS
from app.agents.agent_request.prompt_orchestrator import get_orchestrator_prompt

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
	# input_list.append({"role": "assistant", "content": "What type of keyboard are you looking for? Do you have any specific preferences like brand, mechanical or membrane, wired or wireless, or any special features?"})
	# input_list.append({"role": "user", "content": "Qwerty Wireless"})
	# input_list.append({"role": "assistant", "content": "Do you have a preference for any specific brand or additional features, such as backlighting or extra function keys? Also, how many units do you need?"})
	# input_list.append({"role": "user", "content": "No"})
# 	input_list.append({'arguments': '{"object_type":"keyboard","object_specs":"Qwerty Wireless"}', 'call_id': 'call_JcwkeFeTugj2PmP0j6bgc23C', 'name': 'call_inventory_agent', 'type': 'function_call', 'id': 'fc_0158da19f2b3d9ad0069dd176c9a488197a68236edd7ff751e', 'status': 'completed'})
# 	input_list.append({"type": "function_call_output", 'call_id': 'call_JcwkeFeTugj2PmP0j6bgc23C', "output": json.dumps({"success": "true", "data": "[\n    {\n        \"asin\": \"B0DL6L189W\",\n        \"title\": \"Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys\",\n        \"object_specs\": \"QWERTY Wireless NUMERIC_KEYPAD APPLE\",\n        \"available\": 1,\n        \"match_score\": 10,\n        \"match_reason\": \"Fully wireless QWERTY keyboard with additional features.\"\n    },\n    {\n        \"asin\": \"B0DL6LV7Q6\",\n        \"title\": \"Magic Keyboard - US English , Bluetooth\",\n        \"object_specs\": \"QWERTY Wireless APPLE\",\n        \"available\": 1,\n        \"match_score\": 9,\n        \"match_reason\": \"Wireless QWERTY keyboard but lacks numeric keypad.\"\n    },\n    {\n        \"asin\": \"B003ELVLKU\",\n        \"title\": \"K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black\",\n        \"object_specs\": \"QWERTY Wired LOGITECH\",\n        \"available\": 1,\n        \"match_score\": 0,\n        \"match_reason\": \"Wired keyboard, does not meet wireless requirement.\"\n    }\n]"})})
# 	input_list.append({"role": "assistant", "content": """Assistant: I found a couple of wireless QWERTY keyboards in stock:

# 1. **Magic Keyboard with Touch ID and Numeric Keypad for Mac Models**
#    - **Specs:** QWERTY Wireless, Numeric Keypad
#    - **Available:** 1 unit
#    - **ASIN:** B0DL6L189W

# 2. **Magic Keyboard - US English, Bluetooth**
#    - **Specs:** QWERTY Wireless
#    - **Available:** 1 unit (does not have a numeric keypad)
#    - **ASIN:** B0DL6LV7Q6

# Would you like to go with one of these options? If yes, please specify which one."""})
# 	input_list.append({"role": "user", "content": "First one, make a request to the manager"})

	prompt = get_orchestrator_prompt(data)

	while True:
		try:
			response = client.responses.create(
				model="gpt-4o-mini",
				instructions = prompt,
				tools=TOOLS,
				input=input_list
			)
		except Exception as e:
			print(f"Error : {e}")
			break
		input_list += response.output
		# print(response.output)
		# print(input_list)

		for item in response.output:
			if item.type == "message":
				print(f"Assistant: {item.content[0].text}")
				# state = {
				# 	"id": item.id,
				# 	"content": item.content[0].text,
				# 	"role": item.role,
				# 	"status": item.status,
				# 	"type": item.type
				# }
				# print(state)
				# return_reponse.append(item.model_dump())
				return_reponse.append(response.output)
				return return_reponse
				# user_answer = input("You: ")
				# input_list.append({"role": "user", "content": user_answer})
				# break

			elif item.type == "function_call":
				# print(f'item model dump : {item.model_dump()}')
				# return_reponse.append(item.model_dump())
				return_reponse.append(response.output)
				func = TOOL_REGISTRY.get(item.name)
				if not func:
					print("Error func")
				# 	return {
				# 	"success": False,
				# 	"error_code": "TOOL_NOT_FOUND",
				# 	"message": f"Tool '{item.name}' not found in registry.",
				# 	"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
				# }
				try:
					parsed = json.loads(item.arguments)
				except JSONDecodeError as e:
					print("Error json loads")
					# log -> print (f"Couldn't load arguments for function_call correctly : {e}")
					# return {
					# 	"success": False,
					# 	"message": "Couldn't load arguments for function_call correctly",
					# 	"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
					# }
				# print(parsed)
				try:
					tool_result = func(**parsed)
				except Exception as e:
					print(f"Error in tool : {e}")
					# log -> print({"error": f"tool {item.name} has raised an error : {e}"})
					# return {
					# 	"success": False,
					# 	"message": "An error has been raised during a tool_call",
					# 	"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
					# }
				input_list.append({
					"type": "function_call_output",
					"call_id": item.call_id,
					"output": json.dumps(tool_result)
				})
				return_reponse.append([{
					"type": "function_call_output",
					"call_id": item.call_id,
					"output": json.dumps(tool_result)
				}])
				# print(item.call_id)
				# print(json.dumps(tool_result))

# openai_api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI(
#   api_key=openai_api_key
# )

# data = {
#     "employee": {
#         "name": "Ricardo",
#         "department": "Marketing",
#         "email": "rafael.nascimento@outlook.be"
#     },
#     "manager": {
#         "name": "Armand",
#         "email": "armandeuarmand@gmail.com"
#     },
#     "ticket": {
#         "id": "#4821",
#         "reason": "Need approvisionnement",
#         "created_at": "08/04/2026"
#     }
# }

# req_input_list = {"role": "user", "content": "Can I get a new keyboard ?"}

# call_orchestrator_agent(client, data, req_input_list)