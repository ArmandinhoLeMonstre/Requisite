tools = [
    {
        "type": "function",
        "name": "get_amz_product_list",
        "description": "Use SerpAPI to look for amazon products on Amazon US website, gives back a list of amazon articles",
        "parameters": {
            "type": "object",
            "properties": {
                "product_info": {
                    "type": "string",
                    "description": "a product to look for in an amazon seach bar e.g. wireless azerty keyboard",
                },
            },
            "required": ["product_info"],
        },
    },
]