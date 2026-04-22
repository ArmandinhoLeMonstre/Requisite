from sqlalchemy.exc import SQLAlchemyError, NoResultFound, DatabaseError
from app.models.user import User
from app.models.group import Group
from app.init_db import engine, Session, select
from app.schemas.user_schemas import UserCreate
from fastapi import HTTPException


def create_user(user: UserCreate, db: Session):
	try:
		existing = db.scalars(select(User).where((User.name == user.name) | (User.email == user.email))).first()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with database")
	if existing:
		if existing.name == user.name:
			raise HTTPException(status_code=400, detail="Name already exists")
		raise HTTPException(status_code=400, detail="Email already exists")
	
	user_stmt = User(
		name= user.name,
		email= user.email,
		role= user.role,
		hashed_password= user.hashed_password
	)

	try:
		db.add(user_stmt)
		db.commit()
		db.refresh(user_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	return user_stmt

def select_user(id: int, db: Session):
	try:
		user = db.scalars(select(User).where(User.id == id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	return(user)

def update_user_group(user_id: int, new_group: int, db: Session):
	try:
		user = db.scalars(select(User).where(User.id == user_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	try:
		db.scalars(select(Group).where(Group.id == new_group)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="Group not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	user.group_id = new_group
	try:
		db.add(user)
		db.commit()
		db.refresh(user)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return user
