from openai import OpenAI
import os
import json
from json import JSONDecodeError
from app.tools.request_tools.registry import TOOL_REGISTRY
from app.tools.request_tools.definitions import TOOLS

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

input_list = [
	{
        "role": "system",
        "content": f"""Here is the current request context. Use this data when calling the email_agent.
        Always pass the complete and updated data to the email_agent when calling it.
        
        {json.dumps(data, indent=2)}
        """
    },

    {"role": "user", "content": "Can I get a new keyboard ?"}
]

while True:
	try:
		response = client.responses.create(
			model="gpt-4o-mini",
			instructions = f"""You are an agent orchestrator responsible for helping users submit formal acquisition requests to their manager.

			Your goal is to guide the user through the process of building a complete, persuasive request to obtain approval for a specific object or resource.

			## Your responsibilities:
			1. **Clarify the request** – Ask what object/resource the user wants to acquire if not already specified.
			2. **Gather justification** – Help the user articulate *why* they need it (business case, urgency, impact).
			3. **Identify constraints** – Understand budget, timeline, and any alternatives already considered.
			4. **Draft the request** – Produce a clear, professional request addressed to the manager.
			5. **Refine if needed** – Adjust tone, detail level, or format based on user feedback.

			## Available tools (sub-agents):
			You have access to 3 specialized agents. Use them at the right moment in the workflow:

			- **inventory_agent** – Call this FIRST to check if the requested object already exists 
			in stock. If it does, inform the user and stop — no request needed.
			
			- **amazon_agent** – Call this to find pricing, product references, and availability 
			for the requested object. Use its output to strengthen the request with concrete data 
			(price, link, delivery time).
			
			- **email_agent** – Call this LAST, only after the user has confirmed the product.
			Use {data} for the first parameter of the tool call, and based on what the user's chooses, send it as the product parameter
			to format and send the final request to the manager.

			## Recommended workflow:
			inventory_agent → (If not in stock) amazon_agent →  user confirms → email_agent

			## Rules:
			- Always check inventory before doing anything else.
			- Never send the email without explicit user confirmation of the draft.
			- Ask one clarifying question at a time if information is missing.
			- Adapt the formality level to the user's context (startup vs. corporate, etc.).
			- If amazon_agent returns multiple options, present them to the user and let them choose.

			## Error handling:
			- If a sub-agent returns "success": false, immediately read the "error_code" and "action" fields.
			- Always follow the instruction in the "action" field — it tells you exactly what to do next.
			- Never ignore a failed response or assume the workflow can continue as normal.
			- If there is no "action" field, inform the user something went wrong and ask how they want to proceed.


			""",
			tools=TOOLS,
			input=input_list
		)
	except Exception as e:
		print(f"Error : {e}")
		break
	input_list += response.output
	print(response.output)

	for item in response.output:
		if item.type == "message":
			print(f"Assistant: {item.content[0].text}")
			user_answer = input("You: ")
			input_list.append({"role": "user", "content": user_answer})
			break

		elif item.type == "function_call":
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
			print(parsed)
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

