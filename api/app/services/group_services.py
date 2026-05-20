from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.group_model import Group
from app.models.user_model import User, UserRole
from app.schemas.group_schemas import GroupCreate
from fastapi import HTTPException, status

import random
import string

from app.logger import logger

async def create_group(current_user: User, db: AsyncSession):
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manager")
	
	group_stmt = Group(
		code= ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
		manager_id= current_user.id
	)

	try:
		db.add(group_stmt)
		await db.commit()
		await db.refresh(group_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	logger.info("group.created", user_id=current_user.id, name=current_user.name, role=current_user.role)

	return (group_stmt)


async def select_group(group_id: int, current_user: User, db: AsyncSession):
	if current_user.role != UserRole.manager and current_user.group_id != group_id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not manager")

	try:
		stmt = await db.scalars(select(Group).where(Group.id == group_id))
		group = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code= 404, detail="Group not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return group


async def join_group(current_user: User, code: str, db: AsyncSession):
	try:
		stmt = await db.scalars(select(Group).where(func.lower(Group.code) == code.lower()))
		group = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code= 404, detail="Code doesn't belong to a group")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	current_user.group_id = group.id

	try:
		await db.commit()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("group.joined", user_id=current_user.id, name=current_user.name, role=current_user.role)

	return group
