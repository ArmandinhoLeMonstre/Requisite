
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.init_db import engine, Session, select
from app.schemas.user_schemas import RequestUser
from fastapi import HTTPException


def create_user(user: RequestUser):
	with Session(engine) as session:
		user_stmt = User(
			name= user.name,
			email= user.email,
			role= user.role,
			hashed_password= user.hashed_password
		)
		try:
			session.add(user_stmt)
			session.commit()
		except SQLAlchemyError:
			raise HTTPException(status_code=500, detail="Error with Database server")
		session.refresh(user_stmt)
		return user_stmt

def select_user(id: int):
	with Session(engine) as session:
		try:
			stmt = select(User).where(User.id == id)
			user = session.scalars(stmt).one()
		except SQLAlchemyError:
			raise HTTPException(status_code=404, detail="User not found")
		return(user)
