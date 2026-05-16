from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import func, select

from app.models.user_model import User
from app.schemas.user_schemas import Token
from app.auth import hash_password, verify_password, create_access_token
from app.config import settings

from datetime import timedelta

from app.logger import logger

async def log_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
	try:
		db_stmt = await db.scalars(select(User).where(func.lower(User.email) == form_data.username.lower()))
		user = db_stmt.first()
	except SQLAlchemyError as e:
		logger.error("token.create.error", error=str(e), step="check_user_exists")
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	if not user or not verify_password(form_data.password, user.hashed_password):
		logger.error("token.create.user_credentials_error", step="verify password or user")
		raise HTTPException(
			status_code= status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect email or password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	if not user.email_verified:
		logger.error("token.create.user_credentials_error", step="verify email")
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Email adress unverified, please check your emails"
		)

	access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
	access_token = create_access_token(
		data={"sub": str(user.id)},
		expires_delta=access_token_expires,
	)

	logger.info("token.created", user_id=user.id)
	
	return Token(
		access_token=access_token,
		token_type="bearer"
	)