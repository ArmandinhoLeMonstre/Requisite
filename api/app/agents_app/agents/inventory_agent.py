from app.agents_app.openai_client import client
import os
import json
from json import JSONDecodeError

from app.database import AsyncSessionLocal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.stock_model import Stock
from app.models.stock_common_model import StockCommon

from app.agents_app.agents_exceptions import SubAgentError

async def get_manager_items(manager_id: int):
	async with AsyncSessionLocal() as db:
		try:
			items = None

			stmt = await db.execute(
				select(StockCommon)
			)
			total_common_items = stmt.scalars().all()
			items = [
				{
					"item": item.title,
					"object_type": item.object_type,
					"object_specs": item.object_specs,
					"quantity": item.quantity
				}
				for item in total_common_items
			]

			stmt = await db.execute(
				select(Stock)
				.where(Stock.manager_id == manager_id)
			)
			total_manager_items = stmt.scalars().all()

			if total_manager_items:
				items_manager = [
					{
						"item": item.title,
						"object_type": item.object_type,
						"object_specs": item.object_specs,
						"quantity": item.quantity
					}
					for item in total_manager_items
				]
				items.extend(items_manager)

			return items
		except SQLAlchemyError as e:
			raise

async def call_inventory_agent(manager_id: int, object_type: str, object_specs: str):
	if not object_type:
		return {
			"success": False,
			"error_code": "MISSING_ARGUMENT",
			"field": "object_type",
			"message": "The object type is required to check the inventory.",
			"action": "Ask the user what type of object they want to acquire."
		}
	if not object_specs:
		return {
			"success": False,
			"error_code": "MISSING_ARGUMENT",
			"field": "object_specs",
			"message": "The object specs are required to check the inventory",
			"action": "Ask the user what type of specs the object has."
		}
	if not manager_id:
		return {
			"success": False,
			"error_code": "MISSING_ARGUMENT",
			"field": "manager_id",
			"message": "Manager's id is needed to check the inventory",
			"action": "Tell the user and internal error has occurred"
		}

	try:
		items = await get_manager_items(manager_id)
	except Exception as e:
		raise SubAgentError(
			message=str(e),
			agent= "inventory_agent",
			action= """Inform the user that there is a problem with the inventory agent. 
			Do not proceed automatically. 
			Present the following options and wait for their choice: (1) Try again later, (2) Contact the Amazon agent""",
			step="get_manager_items"
		)
	
	inventory_json = json.dumps(items) #Si jenleve ca, ca crash, a tester pour apres la gestion d'erreur

	input_list = [
		{
			"role": "user",
			"content": f"""The user is looking for a {object_type} with these specs: {object_specs}.
			Here is the current inventory: {inventory_json}.
			Rank the items from best to worst match based on the specs.
			Exclude items that do not match at all.
			Return ONLY a raw JSON array, no markdown, no backticks, no preamble.
			Add a 'match_score' (0-10) and 'match_reason' field to each item."""
		}
	]

	try:
		ranked_response = await client.responses.create(
			model="gpt-4o-mini",
			instructions="You are an inventory ranking agent. Rank products by how well they match the user's specs. Never invent specs that are not in the item data.",
			input=input_list
		)
	except Exception as e:
		raise SubAgentError(
			message=str(e),
			agent= "inventory_agent",
			action= """Inform the user that there is a problem with the inventory agent. 
			Do not proceed automatically. 
			Present the following options and wait for their choice: (1) Try again later, (2) Contact the Amazon agent""",
			step="OpenAI call"
		)

	try:
		ranked_text = ranked_response.output[0].content[0].text
	except (IndexError, AttributeError):
		raise SubAgentError(
			message="Unexpected response structure",
			agent="inventory_agent",
			action= """Inform the user that there is a problem with the inventory agent. 
			Do not proceed automatically. 
			Present the following options and wait for their choice: (1) Try again later, (2) Contact the Amazon agent""",
			step="parsing OpenAI response"
		)

	return {
		"success": True,
		"data": ranked_text
	}