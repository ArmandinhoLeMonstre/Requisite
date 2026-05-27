import os
import json
from openai import AsyncOpenAI
import httpx
import asyncio
from app.agents_app.agents_exceptions import SubAgentError

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)


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

async def product_match(specification, product):
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
        response = await client.responses.create(
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
    
async def get_match_list(specification: dict, product_list: dict):
    organic = product_list.get("organic_results", [])
    
    tasks = [get_product_detail(item["asin"]) for item in organic]
    details = await asyncio.gather(*tasks)
    
    matches = []
    for item, detail in zip(organic, details):
        if isinstance(detail, dict) and "error" in detail:
            continue
        match = await product_match(specification, detail)
        if isinstance(match, dict) and match.get("result"):
            matches.append(item)
        if len(matches) == 3:
            break
    
    return matches

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
