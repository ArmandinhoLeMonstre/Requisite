from app.models.input_model import InputList
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException, status
import json

from app.logger import logger

async def save_input_list(db, ticket_id: int, new_input_list: str):
	try:
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
	except SQLAlchemyError as e:
		logger.error("orchestrator_input_list.save", error=str(e), step="add_input_list_in_db")
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with database")

	logger.info("orchestrator_input_list.saved", ticket_id=ticket_id)

	return 0

async def retrieve_input_list(db: AsyncSession, ticket_id: int):
	try:
		stmt = select(InputList).where(InputList.id == ticket_id)
		result = await db.execute(stmt)
		existing_input_list = result.scalars().first()
	except SQLAlchemyError as e:
		logger.error("orchestrator_input_list.retrieve", error=str(e), step="retrieve_input_list_from_db")
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with database")

	if existing_input_list is None:
		logger.info("orchestrator_input_list.retrieve", ticket_id=ticket_id, message="No input list")
		return None

	restored_input_list = json.loads(existing_input_list.data)

	logger.info("orchestrator_input_list.retrieved", ticket_id=ticket_id)

	return restored_input_list