from app.agents_app.openai_client import client
from app.agents_app.tools.purchase_tools.functions import get_amz_product_list, get_match_list
from app.agents_app.agents_exceptions import SubAgentError


async def call_amazon_agent(object_type: str, object_specs: str):
    data = {
        "object_type": object_type,
        "object_specs": object_specs,
    }

    try:
        product_list = await get_amz_product_list(f"{object_type} {object_specs}")
        matches = await get_match_list(data, product_list)
    except SubAgentError:
        raise
    except Exception as e:
        raise SubAgentError(
            message=str(e),
            agent="amazon_agent",
            action="Inform the user that there is a problem with the Amazon agent, they can retry later",
            step="search and match"
        )

    return {
        "found": len(matches) > 0,
        "results": [
            {
                "name": m.get("title"),
                "price": m.get("price"),
                "link": m.get("link_clean"),
                "thumbnail": m.get("thumbnail"),
                "description": "",
            }
            for m in matches
        ] if matches else None
    }