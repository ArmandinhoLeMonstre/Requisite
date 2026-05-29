import os
import json
import httpx
import asyncio
from app.agents_app.agents_exceptions import SubAgentError
from app.agents_app.openai_client import client
from app.logger import logger


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
                logger.warning("get_product_detail.error", asin=asin, error=result["error"])
                return {"error": result["error"]}
    except Exception as e:
        logger.warning("get_product_detail.exception", asin=asin, error=str(e))
        return {"error": str(e)}
    return result


async def batch_match(specification: dict, products: list) -> list:
    logger.info("batch_match.started", product_count=len(products))

    prompt = (
        f"Specifications: {json.dumps(specification)}\n\n"
        f"Products:\n{json.dumps(products)}\n\n"
        "Return a JSON array of indices (0-based) of the products that match "
        "ALL specifications. Maximum 3. Example: [0, 2]"
    )

    try:
        response = await client.responses.create(
            model="gpt-4o-mini",
            instructions="Reply ONLY with a raw JSON array of integers. No markdown, no backticks, no explanation. Example: [0, 1, 2]",
            input=[{"role": "user", "content": prompt}]
        )
        indices = json.loads(response.output_text)

        if not isinstance(indices, list):
            logger.warning("batch_match.invalid_response", response=response.output_text)
            return []

        matches = []
        for i in indices[:3]:
            if i < len(products):
                matches.append(products[i]["item"])

        logger.info("batch_match.completed", matches_found=len(matches))
        return matches

    except Exception as e:
        logger.error("batch_match.error", error=str(e))
        return []


async def get_match_list(specification: dict, product_list: dict):
    MAX_PRODUCTS = 5
    organic = product_list.get("organic_results", [])[:MAX_PRODUCTS]
    logger.info("get_match_list.started", organic_count=len(organic))

    tasks = [get_product_detail(item["asin"]) for item in organic]
    details = await asyncio.gather(*tasks)

    valid_pairs = []
    for item, detail in zip(organic, details):
        if isinstance(detail, dict) and "error" not in detail:
            valid_pairs.append({"item": item, "detail": detail})

    logger.info("get_match_list.valid_pairs", valid_count=len(valid_pairs))

    if not valid_pairs:
        return []

    return await batch_match(specification, valid_pairs)


async def get_amz_product_list(product_info):
    logger.info("get_amz_product_list.started", query=product_info)

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
                logger.error("get_amz_product_list.serpapi_error", error=result["error"])
                raise SubAgentError(
                    message=result["error"],
                    agent="amazon_agent",
                    action="Inform the user that there is a problem with the Amazon agent, they have to wait until this is resolved",
                    step="SerpApi error in get_amz_product_list"
                )

            logger.info("get_amz_product_list.completed", result_count=len(result.get("organic_results", [])))
            return result

    except SubAgentError:
        raise
    except Exception as e:
        logger.error("get_amz_product_list.exception", error=str(e))
        raise SubAgentError(
            message=str(e),
            agent="amazon_agent",
            action="Inform the user that there is a problem with the Amazon agent, they can retry later",
            step="SerpApi error in get_amz_product_list"
        )