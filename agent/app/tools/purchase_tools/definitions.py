tools = [
    {
        "type": "function",
        "name": "get_product_info",
        "description": "Get the price, link and thumbnail of an amazon product using its ASIN thanks to serpAPI",
        "parameters": {
            "type": "object",
            "properties": {
                "asin": {
                    "type": "string",
                    "description": "an ASIN e.g. B01N2KFHRS",
                },
            },
            "required": ["asin"],
        },
    },
]