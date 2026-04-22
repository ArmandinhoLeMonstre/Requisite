from sqlalchemy.exc import SQLAlchemyError
from app.models.group import Group
from app.init_db import engine, select, Session
from app.models.user import User, UserRole
from app.schemas.group_schemas import RequestGroup
from fastapi import HTTPException
import random
import string


def create_group(group: RequestGroup, db: Session):
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
	manager.group = group_stmt
	group_stmt.users.append(manager)
	try:
		db.add(group_stmt)
		db.commit()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	db.refresh(group_stmt)
	return (group_stmt)
		