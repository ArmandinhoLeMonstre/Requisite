TOOLS = [
    {
        "type": "function",
        "name": "call_inventory_agent",
        "description": "Calling inventory agent to check if user's object is in stock",
        "parameters": {
            "type": "object",
            "properties": {
				"manager_id": {
                    "type": "integer",
                    "description": "Manager's id from the initial data of the request",
                },
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
                "data": {
                    "type": "object",
                    "description": "The request data to draft an email",
					"properties": {
						"employee" : {
							"type": "object",
							"properties": {
								"name": {
									"type": "string"
								},
								"department": {
									"type": "string"
								},
								"email": {
									"type": "string"
								},
							},
							"required": ["name", "department", "email"]
						},
						"manager": {
							"type": "object",
							"properties": {
								"name": {
									"type": "string"
								},
								"email": {
									"type": "string"
								},
							},
							"required": ["name", "email"]
						},
						"ticket": {
							"type": "object",
							"properties": {
								"id": {
									"type": "string"
								},
								"reason": {
									"type": "string"
								},
								"created_at": {
									"type": "string"
								},
							},
							"required": ["id", "reason", "created_at"]
						}
					},
					"required": ["employee", "manager", "ticket"]
                },
				"product": {
					"type": "object",
					"description": "The actual product that the user wants",
					"properties": {
						"name": {
							"type": "string"
						},
						"source": {
							"type": "string"
						},
						"price": {
							"type": "number"
						},
						"link": {
							"type": "string"
						}
					},
					"required": ["name", "source", "price", "link"]
				}
            },
            "required": ["data", "product"],
        },
    },
]
