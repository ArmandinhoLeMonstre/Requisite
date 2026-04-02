tools = [
    {
        "type": "function",
        "name": "get_amazon_product",
        "description": "Use SerpAPI to look for amazon products on Amazon US website, gives back multiple amazon articles",
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