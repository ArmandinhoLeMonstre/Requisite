from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from fastapi import HTTPException, status

from app.models.chat_model import Chat, Sender
from app.models.ticket_model import Ticket, TicketStatus
from app.models.user_model import User
from app.schemas.chat_schemas import ChatResponse, ChatRequest
from app.schemas.ticket_schemas import TicketResponse
from app.services.user_services import CurrentUser

from app.logger import logger

async def new_message(chat: ChatRequest, db: AsyncSession, ticket: TicketResponse):
    
	if ticket.status:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Ticket is closed, no further messages can be sent"
		)
  
	chat = Chat(
		ticket_id= ticket.id,
		sender= chat.sender,
		message= chat.message,
	)

	try:
		db.add(chat)
		await db.commit()
		await db.refresh(chat)
	except SQLAlchemyError as e:
		logger.error("chat.add.error", error=str(e), step="commit_in_db")
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	logger.info("chat.added", ticket_id=ticket.id)

	return chat

async def count_chats(ticket: TicketResponse, db: AsyncSession):
	try:
		stmt = await db.execute(
			select(func.count())
			.select_from(Chat)
			.where(Chat.ticket_id == ticket.id)
		)
		chats = stmt.scalar()
	except Exception as e:
		logger.error("object.create.error", error=str(e), step="check_current_manager_objects")
		raise(HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with database"))

	if chats >= 20 :
		print("OUIIIII")
		try:
			stmt = await db.execute(
				update(Ticket)
				.where(Ticket.id == ticket.id)
				.values(status=TicketStatus.pending)
				.returning(Ticket.id)
			)
			await db.commit()
		except SQLAlchemyError as e:
			logger.error("Update Ticket error", error=str(e), step="Retrieve Ticket in count_chat")
			raise HTTPException(status_code=500, detail="Error with Database server")

	return