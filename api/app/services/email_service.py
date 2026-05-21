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
		"html": f"""
				<div style="max-width:560px; margin:0 auto; font-family:Arial, sans-serif; background:#ffffff; border-radius:12px; overflow:hidden; border:1px solid #e5e7eb;">
					<div style="height:4px; background:#4F46E5;"></div>
					<div style="padding:3rem 2.5rem 2rem;">
						<h2 style="font-size:20px; font-weight:500; color:#1a1a1a; margin:0 0 1.5rem;">Verify your email address</h2>
						<p style="font-size:14px; color:#6b7280; margin:0 0 2.5rem; line-height:1.8;">
							Welcome to Requisite. Click the button below to verify your email address and activate your account.
						</p>
						<a href="http://localhost:5173/verification/{confirmation_token}"
						style="display:inline-block; background:#4F46E5; color:white; padding:14px 32px; border-radius:8px; text-decoration:none; font-size:14px; font-weight:500;">
							Verify my email
						</a>
						<div style="margin-top:3rem; padding-top:2rem; border-top:1px solid #e5e7eb;">
							<p style="font-size:12px; color:#9ca3af; margin:0 0 1rem; line-height:1.8;">
								If the button doesn't work, copy and paste this link into your browser:<br>
								<span style="color:#4F46E5; word-break:break-all;">http://localhost:5173/verification/{confirmation_token}</span>
							</p>
							<p style="font-size:12px; color:#9ca3af; margin:0;">
								<em>If you did not create an account, you can safely ignore this email.</em>
							</p>
						</div>
					</div>
				</div>
				""",
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