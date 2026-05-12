from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from fastapi import HTTPException, status

from app.models.chat_model import Chat, Sender
from app.models.ticket_model import Ticket
from app.models.user_model import User
from app.schemas.chat_schemas import ChatResponse, ChatRequest
from app.services.user_services import CurrentUser

from app.logger import logger

async def new_message(chat: ChatRequest, db: AsyncSession, ticket: Ticket):
	chat = Chat(
		ticket_id= ticket.id,
		sender= chat.sender,
		message= chat.message,
	)

	try:
		chat.ticket = ticket
		db.add(chat)
		await db.commit()
		await db.refresh(chat)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("chat.added", ticket_id=ticket.id)

	return chat