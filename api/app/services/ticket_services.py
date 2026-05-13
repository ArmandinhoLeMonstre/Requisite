from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from fastapi import HTTPException, status
from sqlalchemy import select

from openai import AsyncOpenAI
import os

from app.models.user_model import User, UserRole
from app.models.ticket_model import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import TicketCreate
from app.services.chat_services import new_message, Sender

from app.logger import logger

openai_api_key = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
  api_key=openai_api_key
)

async def create_title(user_message: str):
	prompt = """You are a conversation title generator. When given a user's first message, generate a short sidebar title for the conversation — exactly like Claude does on claude.ai.

	context: 
	This a ticket made from an employee to his manager, keep in mind that those are requests whithin a company department (e.g. "Request for new keyboard" ,not "Keyboard shopping tips and option")

	Style rules:
	- 3 to 6 words maximum
	- Sentence case: only capitalize the first word (and proper nouns)
	- No punctuation at the end
	- No quotes
	- Noun phrase style (e.g. "LLM sidebar title generation", not "Generate LLM sidebar titles")
	- Be specific and descriptive, not generic
	- Capture the core topic or intent

	Respond with the title only. Nothing else."""

	response = await client.responses.create(
		model="gpt-4o-mini",
		instructions=prompt,
		input=user_message
	)

	title = response.output_text

	return title

async def create_ticket(user_message, current_user: User,  db: AsyncSession):
	if current_user.group_id is None and current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not in a group")
	
	ticket_title = await create_title(user_message)
	
	ticket_stmt = Ticket(
		status= TicketStatus.opened,
		user_id= current_user.id,
		description=ticket_title
	)
	
	try:
		db.add(ticket_stmt)
		await db.commit()
		await db.refresh(ticket_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with Database server")

	logger.info("ticket.created", user_id=current_user.id, ticket_id=ticket_stmt.id)
	return ticket_stmt


async def select_ticket(ticket_id: uuid.UUID, user: User, db: AsyncSession):
	try:
		stmt = await db.scalars(select(Ticket).where(Ticket.id == ticket_id))
		ticket = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with Database server")
	
	if user.id != ticket.user_id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Not authorized to see this ticket"
		)
	
	logger.info("ticket.seen", user_id=user.id, ticket_id=ticket_id)
	
	return ticket

async def get_tickets(user: User, db: AsyncSession):
	try:
		stmt = await db.scalars(select(Ticket).where(Ticket.user_id == user.id))
		tickets = stmt.all()
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with database server")
	
	return tickets
