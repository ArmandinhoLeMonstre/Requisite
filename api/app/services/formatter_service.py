from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage

def format_output_message(response: ResponseOutputMessage):
	new_input = {}

	json_resp = response.model_dump()
	content = json_resp.get('content')
	orchestrator_message = content[0].get('text')

	new_input = {
		"role" : "assistant",
		"content" : orchestrator_message
	}

	return new_input

def format_function_tool_call(response: ResponseFunctionToolCall):
	json_resp = response.model_dump()
	return json_resp

def format_orchestrator_message(orchestrator_response: list):

	final_message = []

	for sublist in orchestrator_response:
		for item in sublist:
			if isinstance(item, ResponseFunctionToolCall):
				new_input = format_function_tool_call(item)
				final_message.append(new_input)
			elif isinstance(item, ResponseOutputMessage):
				new_input = format_output_message(item)
				final_message.append(new_input)
			elif isinstance(item, dict):
				final_message.append(item)

	return final_message