import os
import resend
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.models.user_model import User
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger

resend.api_key = os.environ["RESEND_API_KEY"]

async def send_registration_confirmation_email(user_email: str, confirmation_token: str):

	params: resend.Emails.SendParams = {
		"from": "Acme <onboarding@resend.dev>",
		"to": ["armandinho13@yahoo.com"], #ici mettre user email une fois qu'on aura un nom de domaine
		"subject": "Requisit verification link",
		"html": f"<strong>Here is your verification link, http://localhost:5173/verify/{confirmation_token}</strong>",
	}

	email = resend.Emails.send(params)

async def confirm_email(token: str, db: AsyncSession):

	try:
		stmt = await db.execute(
			update(User)
			.where(User.email_verification_token == token)
			.values(email_verified=True, email_verification_token=None)
			.returning(User.id)
		)
	except SQLAlchemyError as e:
		logger.error("email.confirm.error", error=str(e), step="Retrieve user informations")
		raise HTTPException(status_code=500, detail="Error with Database server")

	updated = stmt.first()

	if not updated:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid or expired token")
	
	try:
		await db.commit()
	except SQLAlchemyError as e:
		logger.error("email.confirm.error", error=str(e), step="commit updated user in db")
		raise HTTPException(status_code=500, detail="Error with database")

	logger.info("user.email.verified")

	return {"message": "Email verified successfully"}