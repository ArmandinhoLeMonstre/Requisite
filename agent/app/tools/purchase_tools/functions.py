import os
import serpapi

serp_client = serpapi.Client(api_key = os.getenv("SERPAPI_API_KEY"))

def get_amazon_product(product_info):
	try:
		results = serp_client.search({
			"engine" : "amazon",
			"k" : product_info,
			"json_restrictor" : "organic_results[].{title, link_clean, thumbnail, extracted_price, reviews}"
		})
	except Exception as e:
		return str(e)
	return results