import os
import json
import httpx
import asyncio
from app.agents_app.agents_exceptions import SubAgentError
from app.agents_app.openai_client import client


async def get_product_detail(asin):
    try:
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            response = await http_client.get("https://serpapi.com/search", params={
                "engine": "amazon_product",
                "asin": asin,
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "json_restrictor": "product_results.{price}, about_item[]"
            })
            result = response.json()
            if "error" in result:
                return {"result": False, "error": result["error"]}
    except Exception as e:
        return {"result": False, "error": str(e)}
    return result

async def batch_match(specification: dict, products: list) -> list:
    prompt = (
        f"Specifications: {json.dumps(specification)}\n\n"
        f"Products:\n{json.dumps(products)}\n\n"
        "Return a JSON array of indices (0-based) of the products that match "
        "ALL specifications. Maximum 3. Example: [0, 2]"
        instructions="Reply ONLY with a raw JSON array of integers. No markdown, no code fences, no backticks, no explanation. Example output: [0, 1, 2]"
    )
    try:
        response = await client.responses.create(
            model="gpt-4o-mini",
            instructions="Reply only with a JSON array of matching indices.",
            input=[{"role": "user", "content": prompt}]
        )
        indices = json.loads(response.output_text)
        if not isinstance(indices, list):
            return []
        return [products[i][0] for i in indices[:3] if i < len(products)]
    except Exception as e:
        print(f"batch_match error: {e}")
        return []
    
async def get_match_list(specification: dict, product_list: dict):
    organic = product_list.get("organic_results", [])
    
    tasks = [get_product_detail(item["asin"]) for item in organic]
    details = await asyncio.gather(*tasks)
    
    valid_pairs=[]
    for item, detail in zip(organic, details):
        if (isinstance(detail, dict) and "error" not in detail):
            valid_pairs.append((item, detail))
    
    if not valid_pairs:
        return []
    
    return await batch_match(specification, valid_pairs)

async def get_amz_product_list(product_info):
    try:
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            response = await http_client.get("https://serpapi.com/search", params={
                "engine": "amazon",
                "api_key": os.getenv("SERPAPI_API_KEY"),
                "k": product_info,
                "json_restrictor": "organic_results[].{asin, title, link_clean, thumbnail, price}, serpapi_pagination"
            })
            result = response.json()
            if "error" in result:
                raise SubAgentError(
                    message=result["error"],
                    agent="amazon_agent",
                    action="Inform the user that there is a problem with the Amazon agent, they have to wait until this is resolved",
                    step=f"SerpApi error in get_amz_product_list "
                )
            return result
    except Exception as e:
        raise SubAgentError(
            message=str(e),
            agent="amazon_agent",
            action="Inform the user that there is a problem with the Amazon agent, they can retry later",
            step="SerpApi error in get_amz_product_list"
        )
