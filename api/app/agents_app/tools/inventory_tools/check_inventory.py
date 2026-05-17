def check_inventory(object_type: str):
	if not object_type:
		return {"error": "missing object_type"}
	#ici, admettons que le user tape keyboard mais que la categorie est keyboards, il faudra
	# un agent qui va clarifier la categorie, ou bien donner un nbr de categories 
	# predefinies au premier agent
	inventory = {
		"keyboard": [
			{
				"title" : "Magic Keyboard - US English , Bluetooth",
				"object_specs": "QWERTY Wireless APPLE",
				"object_type": "keyboard",
				"available" : 1
			},
			{
				"title": "Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys",
				"object_specs": "QWERTY Wireless NUMERIC_KEYPAD APPLE",
				"object_type": "keyboard",
				"available" : 1
			},
			{
				"title": "K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black",
				"object_specs": "QWERTY Wired LOGITECH",
				"object_type": "keyboard",
				"available" : 1
			}
		],
		"mouse" : [
			{
				"title": "Magic Mouse - White Multi-Touch Surface ​​​​​​​",
				"object_specs": "Wireless bluetooth",
				"object_type": "keyboard",
				"available" : 1
			},
			{
				"title": "Optical Mouse MS116 (275-BBCB)",
				"object_specs": "Wried Logitech",
				"object_type": "keyboard",
				"available" : 1
			}
		]
	}
	final_category = None
	for category in inventory:
		if category == object_type:
			final_category = category
			break

	if final_category == None:
		return {"invalid_request" : "object_category doesn't exists"}

	c = inventory.get(final_category)
	return c

# x = check_inventory(request={"id" : 1, "object_type" : "keyboard"})
# print(x)
