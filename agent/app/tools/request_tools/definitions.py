TOOLS = [
    {
        "type": "function",
        "name": "call_inventory_agent",
        "description": "Calling inventory agent to check if user's object is in stock",
        "parameters": {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "The type of the actual object in one word",
                },
				"object_specs": {
					"type": "string",
					"description": "The specs of the actual object"
				}
            },
            "required": ["object_type", "object_specs"],
        },
    },
	{
        "type": "function",
        "name": "call_amazon_agent",
        "description": "Calling Amazon agent to search the user's product on Amazon is the product is not in stock",
        "parameters": {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "The type of the actual object in one word",
                },
				"object_specs": {
					"type": "string",
					"description": "The specs of the actual object"
				}
            },
            "required": ["object_type", "object_specs"],
        },
    },
		{
        "type": "function",
        "name": "call_email_agent",
        "description": "Calling email agent to draft and send a formal acquisition request to the manager for the specified object",
        "parameters": {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "The type of the actual object in one word",
                },
				"object_specs": {
					"type": "string",
					"description": "The specs of the actual object"
				}
            },
            "required": ["object_type", "object_specs"],
        },
    },
]
