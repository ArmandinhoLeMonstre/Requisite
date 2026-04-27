def check_inventory(object_type: str):
	if not object_type:
		return {"error": "missing object_type"}
	#ici, admettons que le user tape keyboard mais que la categorie est keyboards, il faudra
	# un agent qui va clarifier la categorie, ou bien donner un nbr de categories 
	# predefinies au premier agent
	inventory = {
		"keyboard": [
			{
				"asin" : "B0DL6LV7Q6",
				"title" : "Magic Keyboard - US English , Bluetooth",
				"object_specs": "QWERTY Wireless APPLE",
				"avalable" : 1
			},
			{
				"asin": "B0DL6L189W",
				"title": "Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys",
				"object_specs": "QWERTY Wireless NUMERIC_KEYPAD APPLE",
				"avalable" : 1
			},
			{
				"asin": "B003ELVLKU",
				"title": "K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black",
				"object_specs": "QWERTY Wired LOGITECH",
				"avalable" : 1
			}
		],
		"mouse" : [
			{
				"asin": "B0DL72PK1P",
				"title": "Magic Mouse - White Multi-Touch Surface ​​​​​​​",
				"price": 63.99,
				"avalable" : 1
			},
			{
				"asin": "B012DT5U96",
				"title": "Optical Mouse MS116 (275-BBCB)",
				"price": 7.99,
				"avalable" : 1
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
