from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.models.group import Group
from app.init_db import engine, select, Session
from app.models.user import User, UserRole
from app.schemas.group_schemas import GroupCreate
from fastapi import HTTPException
import random
import string


def create_group(group: GroupCreate, db: Session):
	try:
		manager = db.scalars(select(User).where(User.id == group.manager_id)).one()
	except SQLAlchemyError:
		raise HTTPException(status_code=404, detail="User not found")
	if manager.role != UserRole.manager:
		raise HTTPException(status_code=403, detail="User is not a manager")
	
	group_stmt = Group(
		code= ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
		manager_id= group.manager_id
	)

	try:
		manager.group = group_stmt
		db.add(group_stmt)
		db.commit()
		db.refresh(group_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return (group_stmt)


def select_group(group_id: int, db: Session):
	try:
		group = db.scalars(select(Group).where(Group.id == group_id)).one()
	except NoResultFound:
		raise HTTPException(status_code= 404, detail="Group not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return group