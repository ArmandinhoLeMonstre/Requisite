from openai import OpenAI
import os
import json
from app.tools.registry import TOOL_REGISTRY
from app.tools.definitions import TOOLS

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=openai_api_key
)

input_list = [
    {"role": "user", "content": "Can I get a new keyboard ?"}
]

parsed = {'user_id': None, 'object_type': None, 'purpose': None}

while True:
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=f"""You need to fill the text part with values from the input. 
						If you are uncertain, keep null. 
						This is the current state : {parsed}. 
						Do not change values that are not null""",
        input=input_list,
        text={"format": {"type": "json_schema", "name": "request_params", "strict": True, "schema": {
            "type": "object_type",
            "properties": {
                "user_id": {"type": ["number", "null"]},
                "object_type": {"type": ["string", "null"]},
                "purpose": {"type": ["string", "null"]}
            },
            "required": ["user_id", "object_type", "purpose"],
            "additionalProperties": False
        }}}
    )

    input_list += response.output
    print(f'response output : {response.output}')
    parsed = json.loads(response.output[0].content[0].text)
    print(f"Current state: {parsed}")

    if all(value is not None for value in parsed.values()):
        break

    # missing = [key for key, value in parsed.items() if value is None]
    missing = []
    for key,value in parsed.items():
        if value is None:
            missing.append(key)

    question_response = client.responses.create(
        model="gpt-4o-mini",
        instructions="You are a helpful assistant. Ask the user for the missing information in a natural, friendly way.",
        input=input_list + [
            {"role": "user", "content": f"The following fields are missing: {missing}. Ask the user for them."}
        ]
    )

    question = question_response.output[0].content[0].text
    print(f"Assistant: {question}")
    user_answer = input("You: ")

    input_list.append({"role": "user", "content": user_answer})
