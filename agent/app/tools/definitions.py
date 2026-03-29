TOOLS = [
    {
        "type": "function",
        "name": "check_budget",
        "description": "Get user's remaining budget.",
		"parameters": {
			"type": "object",
			"properties": {
				"employee_id": {
					"type": "integer",
					"description": "The employee's id"
				}
			},
        "required": ["employee_id"]
    	}
    },
	{
        "type": "function",
        "name": "check_policy",
        "description": "Check if the user grade can acquire this type of material",
		"parameters": {
			"type": "object",
			"properties": {
				"employee_id": {
					"type": "integer",
					"description": "The employee's id"
				},
				"material_type": {
					"type": "string",
					"description": "Type of the material"
				}
			},
        "required": ["employee_id", "material_type"]
    	}
    },
	{
        "type": "function",
        "name": "get_material_type",
        "description": "Define the type of material that the user wants",
		"parameters": {
			"type": "object",
			"properties": {
				"employee_id": {
					"type": "integer",
					"description": "The employee's id"
				},
				"object": {
					"type": "string",
					"description": "The object that the user requests"
				}
			},
        "required": ["employee_id", "object"]
    	}
    }
]