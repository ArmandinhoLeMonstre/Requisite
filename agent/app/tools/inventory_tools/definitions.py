TOOLS = [
	{
        "type": "function",
        "name": "check_inventory",
        "description": "Get current inventory stock to see if user's object type is in stock",
		"parameters": {
			"type": "object",
			"properties": {
				"request": {
					"type": "object",
					"description": "The current inventory where you can look for available objects",
					"properties": {
						"user_id": {"type": "number"},
						"object_type": {"type": "string"},
						"purpose":  {"type": "string"}
					},
					"required": ["user_id", "object_type", "purpose"]
				}
			},
        "required": ["request"]
    	}
    },
]