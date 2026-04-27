from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from fastapi import HTTPException, status

from app.models.chat import Chat, Sender
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.chat_schemas import ChatResponse
from app.services.user_services import CurrentUser


def new_message(sending: Sender, db: Session, ticket: Ticket, msg: str):
	chat = Chat(
		ticket_id= ticket.id,
		sender= sending,
		message= msg,
	)

	try:
		chat.ticket = ticket
		db.add(chat)
		db.commit()
		db.refresh(chat)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return chat