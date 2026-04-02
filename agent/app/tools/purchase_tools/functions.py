import os
import serpapi
import json

def get_product_info(asin):
	serp_client = serpapi.Client(api_key = os.getenv("SERPAPI_API_KEY"))
	try:
		results = serp_client.search({
			"engine" : "amazon",
			"k" : asin,
		})
	except Exception as e:
		return str(e)
	try:
		product = {
			"price": results["organic_results"][0]["price"],
			"link": results["organic_results"][0]["link"],
			"thumbnail": results["organic_results"][0]["thumbnail"]
		}
	except:
		return "Index error in 'results['organic_results'][0]'"
	return json.dumps(product)