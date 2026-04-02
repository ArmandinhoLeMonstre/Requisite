from openai import OpenAI
import os
import json
from app.tools.request_tools.registry import TOOL_REGISTRY
from app.tools.request_tools.definitions import TOOLS

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=openai_api_key
)

input_list = [
    {"role": "user", "content": "Can I get a new keyboard ?"}
]

while True:
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
		
		- **email_agent** – Call this LAST, only after the user has confirmed the draft, 
		to format and send the final request to the manager.

		## Recommended workflow:
		inventory_agent → (If not in stock) amazon_agent → draft request → user confirms → email_agent

		## Rules:
		- Always check inventory before doing anything else.
		- Never send the email without explicit user confirmation of the draft.
		- Ask one clarifying question at a time if information is missing.
		- Adapt the formality level to the user's context (startup vs. corporate, etc.).
		- If amazon_agent returns multiple options, present them to the user and let them choose.

		""",
		tools=TOOLS,
		input=input_list
	)
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
			parsed = json.loads(item.arguments)
			print(parsed)
			tool_result = func(**parsed)
			input_list.append({
				"type": "function_call_output",
				"call_id": item.call_id,
				"output": json.dumps(tool_result)
			})

