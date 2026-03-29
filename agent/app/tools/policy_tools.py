def check_policy(employee_id: int):
	policy = {
		"tech" : {
			"junior" : {
				"allowed_categories" : ["hardware"],
				"approval_limit" : 50
			},
			"senior" : {
				"allowed_categories" : ["hardware", "software"],
				"approval_limit" : 100
			}
		},
		"creative" : {
			"junior" : {
				"allowed_categories" : ["hardware", "production"],
				"approval_limit" : 20
			},
			"senior" : {
				"allowed_categories" : ["hardware", "software", "production"],
				"approval_limit" : 100
			}
		}
	}
	return

def get_material_type(employee_id: int, object: str):
	res = None

	available_material = {
		"computer" : "hardware",
		"mouse": "hardware",
		"keyboard": "hardware"
	}

	res = available_material.get(object)

	return res
