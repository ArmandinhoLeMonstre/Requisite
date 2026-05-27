from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import func, select
from app.models.user_model import User, UserRole
from app.models.stock_model import Stock
from app.models.stock_common_model import StockCommon
from app.schemas.inventory_schemas import ObjectRequest

from fastapi import HTTPException, status

from app.logger import logger

async def add_object(object: ObjectRequest, current_user: User, db: AsyncSession):
	if current_user.role != UserRole.manager:
		logger.error("object.create.error", error="user is not manager", step="check_role")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not Manager")
	
	try:
		stmt = await db.execute(
			select(func.count())
			.select_from(Stock)
			.where(Stock.manager_id == current_user.id)
		)
		total_objects = stmt.scalar()
		if total_objects >= 3:
			logger.error("object.create.error", error="Manager has already 3 additionals object", step="check_current_objects")
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inventory is full, cannot add new items.")
	except SQLAlchemyError as e:
		logger.error("object.create.error", error=str(e), step="check_current_manager_objects")
		raise(HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with database"))

	new_object = Stock(
		title=object.title,
		object_type=object.object_type,
		object_specs=object.object_specs,
		quantity=object.quantity,
		manager_id=current_user.id
	)

	try:
		db.add(new_object)
		await db.commit()
		await db.refresh(new_object)
	except SQLAlchemyError as e:
		logger.error("object.create.error", error=str(e), step="add_object_in_db")
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("object.added", manager_id=current_user.id, object_id=new_object.id)

	return None

async def get_user_inventory(current_user: User, db: AsyncSession):
	if current_user.role != UserRole.manager:
		logger.error("inventory.manager.get.error", error="user is not manager", step="check_role")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not Manager")

	try:
		stmt = await db.execute(
			select(Stock)
			.where(Stock.manager_id == current_user.id)
		)
		total_objects = stmt.scalars().all()

	except SQLAlchemyError as e:
		logger.error("inventory.manager.get.error", error=str(e), step="check_current_manager_objects")
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("inventory.manager.get", manager_id=current_user.id)

	return total_objects

async def get_common_inventory(current_user: User, db: AsyncSession):
	if current_user.role != UserRole.manager:
		logger.error("inventory.common.get.error", error="user is not manager", step="check_role")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not Manager")

	try:
		stmt = await db.execute(
			select(StockCommon)
		)
		total_objects = stmt.scalars().all()

	except SQLAlchemyError as e:
		logger.error("inventory.common.get.error", error=str(e), step="check_current_manager_objects")
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("inventory.common.get", manager_id=current_user.id)

	return total_objects

async def delete_user_item(current_user: User, item_id:int, db: AsyncSession):
	if current_user.role != UserRole.manager:
		logger.error("inventory.user.delete.error", error="User is not manager", step="check_current_user_role")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")

	try:
		stmt = await db.scalars(select(Stock).where(Stock.id == item_id))
		item = stmt.one()
	except NoResultFound:
		logger.error("inventory.user.delete.error", error="Item is not in stock", step="check_item_existence")
		raise HTTPException(status_code=404, detail="Item not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	if item.manager_id != current_user.id:
		logger.error("inventory.user.delete.error", error="Item is not from current manager", step="check_item_owner")
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")
	try:
		await db.delete(item)
		await db.commit()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("inventory.user.delete", manager_id=current_user.id, item_id=item_id)