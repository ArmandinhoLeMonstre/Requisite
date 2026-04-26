from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.group import Group
from app.models.user import User, UserRole
from app.schemas.group_schemas import GroupCreate
from fastapi import HTTPException, status

import random
import string


def create_group(group: GroupCreate, current_user: User, db: Session):
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a manager")
	
	group_stmt = Group(
		code= ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
		manager_id= current_user.id
	)

	try:
		current_user.group = group_stmt
		db.add(group_stmt)
		db.commit()
		db.refresh(group_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return (group_stmt)


def select_group(group_id: int, current_user: User, db: Session):
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not manager")

	try:
		group = db.scalars(select(Group).where(Group.id == group_id)).one()
	except NoResultFound:
		raise HTTPException(status_code= 404, detail="Group not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return group


def join_group(current_user: User, code: str, db: Session):
	try:
		group = db.scalars(select(Group).where(func.lower(Group.code) == code.lower())).one()
	except NoResultFound:
		raise HTTPException(status_code= 404, detail="Code doesn't belong to a group")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	current_user.group = group

	return group
