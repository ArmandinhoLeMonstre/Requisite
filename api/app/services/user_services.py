from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.init_db import get_db

from app.models.user_model import User
from app.models.group_model import Group
from app.schemas.user_schemas import UserCreate, UserUpdate, UserRole

from fastapi import HTTPException, status, Depends
from typing import Annotated

from app.auth import hash_password, verify_access_token, oauth2_scheme


def create_user(user: UserCreate, db: Session):
	try:
		existing = db.scalars(select(User).where((func.lower(User.name) == user.name.lower()) | (func.lower(User.email) == user.email.lower()))).first()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with database")
	if existing:
		if existing.name == user.name:
			raise HTTPException(status_code=400, detail="Name already exists")
		raise HTTPException(status_code=400, detail="Email already exists")
	
	new_user = User(
		name= user.name,
		email= user.email.lower(),
		role= user.role,
		hashed_password= hash_password(user.password)
	)

	try:
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	return new_user

def select_user(current_user: User, user_id: int, db: Session):
	if current_user.id == user_id:
		return current_user
	
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to see this user")

	try:
		user = db.scalars(select(User).where(User.id == user_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError as e:
		raise HTTPException(status_code=500, detail="Error with Database server")

	return(user)

def patch_user(current_user: User, user_id: int, new_data: UserUpdate, db: Session):
	REGISTRY = {
		"name": func.lower(User.name),
		"email": func.lower(User.email),
	}

	if current_user.role != UserRole.manager and current_user.id != user_id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

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
				existing = db.scalars(select(User).where((REGISTRY.get(key) == value.lower()) & (User.id != user_id))).first()
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

def delete_user(current_user: User, user_id:int, db:Session):
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this account")

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

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
	user_id = verify_access_token(token)
	if user_id is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid or expired token",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	try:
		user_id_int = int(user_id)
	except (TypeError, ValueError):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid or expired token",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	try:
		user = db.scalars(select(User).where(User.id == user_id_int)).one()
	except NoResultFound:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="User not found",
			headers={"WWW-Authenticate": "Bearer"},
		)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")

	return user

CurrentUser = Annotated[User, Depends(get_current_user)]
