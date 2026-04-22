from sqlalchemy.exc import SQLAlchemyError, NoResultFound, DatabaseError
from app.models.user import User
from app.init_db import engine, Session, select
from app.schemas.user_schemas import RequestUser
from fastapi import HTTPException


def create_user(user: RequestUser, db: Session):
	existing = db.scalars(select(User).where((User.name == user.name) | (User.email == user.email))).first()
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
