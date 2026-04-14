from api.schemas.agents_requests_schemas import OrchestratorRequest
from app.agents.agent_request.agent_initial_request import call_orchestrator_agent
from openai import OpenAI
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage
import os

def sanitize_output_message(response: ResponseOutputMessage):
	new_input = {}

	json_resp = response.model_dump()
	content = json_resp.get('content')
	orchestrator_message = content[0].get('text')

	new_input = {
		"role" : "assistant",
		"content" : orchestrator_message
	}

	return new_input

def sanitize_function_tool_call(response: ResponseFunctionToolCall):
	json_resp = response.model_dump()
	return json_resp

def sanitize_orchestrator_message(orchestrator_response: list):

	final_message = []

	for sublist in orchestrator_response:
		for item in sublist:
			if isinstance(item, ResponseFunctionToolCall):
				new_input = sanitize_function_tool_call(item)
				final_message.append(new_input)
			elif isinstance(item, ResponseOutputMessage):
				new_input = sanitize_output_message(item)
				final_message.append(new_input)
			elif isinstance(item, dict):
				final_message.append(item)
		# print(sublist)
	# print(final_message)

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
			"id": "#6242",
			"reason": "Need approvisionnement",
			"created_at": "08/04/2026"
		}
	}
	req_input_list = [{"role": "user", "content": "Can I get a new keyboard ?"}]
	req_input_list.append({"role": "assistant", "content": "What type of keyboard are you looking for? Do you have any specific preferences like brand, mechanical or membrane, wired or wireless, or any special features?"})
	req_input_list.append({"role": "user", "content": "Qwerty Wireless"})
	req_input_list.append({"role": "assistant", "content": "Do you have a preference for any specific brand or additional features, such as backlighting or extra function keys? Also, how many units do you need?"})
	req_input_list.append({"role": "user", "content": "No"})
	test = {'arguments': '{"object_type":"keyboard","object_specs":"Qwerty Wireless"}', 'call_id': 'call_hPxrO6q0Kbz0mHCEWgVqxjhH', 'name': 'call_inventory_agent', 'type': 'function_call', 'id': 'fc_0d53188b0169a8260069de7c11564c81909a30775863d98a55', 'namespace': None, 'status': 'completed'}, {'type': 'function_call_output', 'call_id': 'call_hPxrO6q0Kbz0mHCEWgVqxjhH', 'output': '{"success": true, "data": "[\\n    {\\n        \\"asin\\": \\"B0DL6LV7Q6\\",\\n        \\"title\\": \\"Magic Keyboard - US English , Bluetooth\\",\\n        \\"object_specs\\": \\"QWERTY Wireless APPLE\\",\\n        \\"avalable\\": 1,\\n        \\"match_score\\": 10,\\n        \\"match_reason\\": \\"Exact match for QWERTY Wireless.\\"\\n    },\\n    {\\n        \\"asin\\": \\"B0DL6L189W\\",\\n        \\"title\\": \\"Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys\\",\\n        \\"object_specs\\": \\"QWERTY Wireless NUMERIC_KEYPAD APPLE\\",\\n        \\"avalable\\": 1,\\n        \\"match_score\\": 9,\\n        \\"match_reason\\": \\"QWERTY Wireless, but includes a numeric keypad which is additional.\\"\\n    },\\n    {\\n        \\"asin\\": \\"B003ELVLKU\\",\\n        \\"title\\": \\"K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black\\",\\n        \\"object_specs\\": \\"QWERTY Wired LOGITECH\\",\\n        \\"avalable\\": 1,\\n        \\"match_score\\": 0,\\n        \\"match_reason\\": \\"Not wireless; does not match user\'s requirement.\\"\\n    }\\n]"}'}, {'role': 'assistant', 'content': 'I found two suitable wireless keyboards available:\n\n1. **Magic Keyboard - US English, Bluetooth**\n   - Specs: QWERTY Wireless\n   - Available: 1 unit\n\n2. **Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys**\n   - Specs: QWERTY Wireless, includes Numeric Keypad\n   - Available: 1 unit\n\nThe first option is a direct match to your request, while the second option includes a numeric keypad. \n\nWould you like to go with the first option, or do you prefer the second one?'}
	req_input_list.extend(test)
	req_input_list.append({"role": "user", "content": "I want number one, send an email for it"})

	orchestrator_response = call_orchestrator_agent(client, data, req_input_list)
	# input_to_append = sanitize_output_message(response)
	# print(input_to_append)
	# Ici je dois faire un return array dans la fct de l'orchestrator qui va me permettre d'avoir tout l'input list qui s'append petit a petit. Ex apres un tool_call append puis apres j'
	# j'append le msg de l'assistant. reteste le code tu verras
	# print(f"response returned by orchestrator : {orchestrator_response}")
	# sanitize_orchestrator_message(orchestrator_response)

	return (0)