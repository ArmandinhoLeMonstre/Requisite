def call_inventory_agent(object_type: str, object_specs: str):
	if not object_type:
		return {"error" : "missing object_type"}
	if not object_specs:
		return {"error" : "missing object_specs"}
	return {"result": {
		"status": "product not found",
		"product": None
	}}