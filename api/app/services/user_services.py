from sqlalchemy.exc import SQLAlchemyError, NoResultFound, DatabaseError
from app.models.user import User
from app.models.group import Group
from app.init_db import engine, Session, select
from app.schemas.user_schemas import UserCreate, UserUpdate
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
		hash_password= user.password
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

def patch_user(user_id: int, new_data: UserUpdate, db: Session):
	REGISTRY = {
		"name": User.name,
		"email": User.email,
	}

	try:
		user = db.scalars(select(User).where(User.id == user_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	update_data = new_data.model_dump(exclude_unset=True)

	for key, value in update_data.items():
		if key == "group_id":
			try:
				db.scalars(select(Group).where(Group.id == value)).one()
			except NoResultFound:
				raise HTTPException(status_code=404, detail="Group not found")
			except SQLAlchemyError:
				raise HTTPException(status_code=500, detail="Error with Database server")
		elif key == "name" or key == "email":
			try:
				existing = db.scalars(select(User).where((REGISTRY.get(key) == value) & (User.id != user_id))).first()
			except SQLAlchemyError:
				raise HTTPException(status_code=500, detail="Error with Database server")
			if existing:
				if key == "name":
					raise HTTPException(status_code=400, detail="Name already exists")
				raise HTTPException(status_code=400, detail="Email already exists")
		setattr(user, key, value)

	try:
		db.commit()
		db.refresh(user)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return user

def delete_user(user_id:int, db:Session):
	try:
		user = db.scalars(select(User).where(User.id == user_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	try:
		db.delete(user)
		db.commit()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")	
