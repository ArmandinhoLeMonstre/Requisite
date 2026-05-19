from openai import AsyncOpenAI
import os
import json
from json import JSONDecodeError

from app.database import AsyncSessionLocal

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.stock_model import Stock

from app.inventory_in_memory import inventory

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)

async def get_manager_items(manager_id: int):
	async with AsyncSessionLocal() as db:
		try:
			items = None

			stmt = await db.execute(
				select(Stock)
				.where(Stock.manager_id == manager_id)
			)
			total_objects = stmt.scalars().all()

			if total_objects:
				items = [
					{
						"item": item.title,
						"object_type": item.object_type,
						"object_specs": item.object_specs,
						"quantity": item.quantity
					}
					for item in total_objects
				]

			return items
		except SQLAlchemyError as e:
			print(e) # gerer les erreurs ici

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

	items = await get_manager_items(manager_id)
	if items:
		inventory.extend(items)
	
	inventory_json = json.dumps(inventory) #Si jenleve ca, ca crash, a tester pour apres la gestion d'erreur

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
		return {
			"success": False,
			"error_code": "API_ERROR",
			"message": "API call to OpenAI failed"
		}

	try:
		ranked_text = ranked_response.output[0].content[0].text
	except (IndexError, AttributeError):
		return {
			"success": False,
			"message": "Unexpected response structure",
			"action": "Retry once. If the error persists, do not proceed automatically. Present the following options to the user and wait for their choice: (1) Try again later, (2) Skip this step and continue, (3) Cancel the request."
		}

	return {
		"success": True,
		"data": ranked_text
	}