def check_inventory(request: dict):
	object_type = request.get("object_type")
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
				"link" : "https://www.amazon.com/Apple-Magic-Keyboard-US-English/dp/B0DL6LV7Q6/ref=sr_1_1?dib=eyJ2IjoiMSJ9.XqUjj-E5FhaEcPG5-YnAen9YcEHrn44Ab9DGrAiE2IRicY9pxsJ7N3cegwb1k_0FpmP3gOjcVAv32cv83UEmDnKNtkH1bkzGNw8pnFVoJCof3SYXHh7AhImSRH3rsyppD9WswuEuIXEdc_dmKV14bRxGuECzRk15xVyGEuc_TdckeNnxFKfk5R9XUKPNe58hlC41gctfI-6OvqM2V2w7zay7fNIHtFaD79OiEOWVOMs.eDcisIO-MNuILm5_G_jBo0cCd3p1N34FsPNkGd-s0Xk&dib_tag=se&keywords=Apple+magic+keyboard&qid=1774972597&sr=8-1",
				"price" : 79.99,
				"avalable" : 1
			},
			{
				"ASIN": "B0DL6L189W",
				"title": "Magic Keyboard with Touch ID and Numeric Keypad for Mac Models with Apple Silicon - US English - Black Keys",
				"link": "https://www.amazon.com/Keyboard-Numeric-Keypad-Apple-Silicon/dp/B0DL6L189W/",
				"price": 187.99,
				"avalable" : 1
			},
			{
				"asin": "B003ELVLKU",
				"title": "K120 Wired Keyboard for Windows, USB Plug-and-Play, Full-Size, Spill-Resistant, Curved Space Bar, Compatible with PC, Laptop - Black",
				"link": "https://www.amazon.com/Logitech-920-002478-K120-USB-Keyboard/dp/B003ELVLKU/",
				"price": 9.79,
				"avalable" : 1
			}
		],
		"mouse" : [
			{
				"ASIN": "B0DL72PK1P",
				"title": "Magic Mouse - White Multi-Touch Surface ​​​​​​​",
				"link": "https://www.amazon.com/Apple-Magic-Mouse-Multi-Touch-Surface/dp/B0DL72PK1P/",
				"price": 63.99,
				"avalable" : 1
			},
			{
				"asin": "B012DT5U96",
				"title": "Optical Mouse MS116 (275-BBCB)",
				"link": "https://www.amazon.com/Dell-Optical-Mouse-MS116-275-BBCB/dp/B012DT5U96/",
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
