from app.models.input_model import InputList
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
import json

async def save_input_list(db, ticket_id: int, new_input_list: str):
	stmt = insert(InputList).values(
	    id=ticket_id, data=new_input_list
	)
	stmt = stmt.on_conflict_do_update(
		index_elements=["id"],
		set_={
			"data": stmt.excluded.data
		}
	)

	await db.execute(stmt)
	await db.commit()

	return 0

async def retrieve_input_list(db: AsyncSession, ticket_id: int):
	stmt = select(InputList).where(InputList.id == ticket_id)
	result = await db.execute(stmt)
	existing_input_list = result.scalars().first()
	if existing_input_list is None:
		return None

	restored_input_list = json.loads(existing_input_list.data)

	return restored_input_list