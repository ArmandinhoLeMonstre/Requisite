
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, DatabaseError
from app.models.user import User
from app.init_db import engine, Session, select
from app.schemas.user_schemas import RequestUser
from fastapi import HTTPException


def create_user(user: RequestUser, db: Session):
	user_stmt = User(
		name= user.name,
		email= user.email,
		role= user.role,
		hashed_password= user.hashed_password
	)
	try:
		db.add(user_stmt)
		db.commit()
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	db.refresh(user_stmt)
	return user_stmt

def select_user(id: int, db: Session):
	try:
		stmt = select(User).where(User.id == id)
		user = db.scalars(stmt).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="User not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	return(user)
