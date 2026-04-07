import os
import serpapi
import json
from openai import OpenAI

op_client = OpenAI()
serp_client = serpapi.Client(api_key = os.getenv("SERPAPI_API_KEY"))

def get_product_detail(asin):
	try:
		result = serp_client.search({
			"engine" :"amazon_product",
			"asin": asin,
			"json_restrictor" : "product_results.{price}, about_item[]"
		})
	except Exception as e:
		return {"result": False, "error": str(e)}
	return result

def	product_match(specification, product):
	input_list = [
		{
			"role": "system",
			"content": "Your role is to see if a product matches perfectly the specifications given, if it does, you return True, if not you return False. If you receive an error send it back with the format 'error: explanation'",
		},
		{
			"role": "user",
			"content": "specification: " + str(specification) + " product detail: " + str(product)
		},
	]
	
	try:
		response = op_client.responses.create(
			model= "gpt-4o-mini",
			instructions= """Reply using the format {"result": boolean, "reasoning": string}, give a super short reasoning.
							reasoning is the reason why it matches or not""",
			input= input_list,
		)
	except Exception as e:
		return {"result": False, "error": str(e)}
	
	try:
		return json.loads(response.output_text)
	except json.JSONDecodeError:
		return {"result": False, "error": "Invalid JSON returned by model"}
	
def get_match_list(specification: dict, product_list):
	product_list = product_list.as_dict()
	matches=[]
	for item in product_list["organic_results"]:
		details = get_product_detail(item["asin"])
		if isinstance(details, dict) and "error" in details:
			continue
		if product_match(specification, details)["result"]:
			matches.append(item)
		if len(matches) == 3:
			break
	return matches

def get_amz_product_list(product_info):
	try:
		results = serp_client.search({
			"engine" : "amazon",
			"k" : product_info,
			"json_restrictor" : "organic_results[].{asin, title, link_clean, thumbnail, price}, serpapi_pagination"
		})
	except Exception as e:
		return str(e)
	return results
