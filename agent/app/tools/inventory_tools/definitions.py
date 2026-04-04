TOOLS = [
	{
        "type": "function",
        "name": "check_inventory",
        "description": "Get current inventory stock to see if user's object type is in stock",
		"parameters": {
			"type": "object",
			"properties": {
				"object_type": {
					"type": "string",
					"description": "The type of the actual object in one word"
				}
			},
        "required": ["object_type"]
    	}
    },
]