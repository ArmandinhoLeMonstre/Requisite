from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from fastapi import HTTPException, status
from sqlalchemy import select

from openai import AsyncOpenAI
import os

from app.models.user_model import User, UserRole
from app.models.group_model import Group
from app.models.ticket_model import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import TicketsGroup, TicketResponse

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
		user_id= current_user.id,
		description=ticket_title
	)
	
	try:
		db.add(ticket_stmt)
		await db.commit()
		await db.refresh(ticket_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with Database server")

	logger.info("ticket.created", user_id=current_user.id, ticket_id=ticket_stmt.id, ticket_title=ticket_title)

	return ticket_stmt


async def select_ticket(ticket_id: uuid.UUID, user: User, db: AsyncSession):
	try:
		stmt = await db.scalars(select(Ticket).where(Ticket.id == ticket_id))
		ticket = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with Database server")
	
	if user.id != ticket.user_id and user.role != UserRole.manager:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Not authorized to see this ticket"
		)
	
	logger.info("ticket.seen", user_id=user.id, ticket_id=ticket_id)
	
	return TicketResponse(status= ticket.status,
                       description=ticket.description,
                       user_id=ticket.user_id,
                       id=ticket.id,
                       user_name=user.name,
                       created_at=ticket.created_at)
 
async def select_chats(ticket_id: uuid.UUID, user: User, db: AsyncSession):
	try:
		stmt = await db.scalars(select(Ticket).where(Ticket.id == ticket_id))
		ticket = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error with Database server")
	
	if user.id != ticket.user_id and user.role != UserRole.manager:
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

async def get_tickets_group(user: User, db: AsyncSession):
	if user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User must be manager")

	try:
		stmt = await db.scalars(select(User).where(User.id == user.id).options(selectinload(User.groups).selectinload(Group.users).selectinload(User.tickets)))
		loaded_user = stmt.one()

		if (not loaded_user.groups):
			return TicketsGroup(chats={})

		result = {}
		for group in loaded_user.groups:
			tickets = []
			for member in group.users:
				for ticket in member.tickets:
					tickets.append(TicketResponse(
						id= ticket.id,
						status=ticket.status,
						description=ticket.description,
      					created_at=ticket.created_at,
						user_name=member.name,
						user_id=member.id
					))
			result[group.code] = tickets
		return TicketsGroup(chats=result)
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

async def change_status(current_user: User,ticket_id: uuid.UUID, new_status: TicketStatus, db:AsyncSession):
	if current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not manager")

	try:
		stmt = await db.scalars(select(Ticket).where(Ticket.id == ticket_id))
		ticket = stmt.one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
     
	ticket.status = new_status
	try:
		await db.commit()
		await db.refresh(ticket)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return ticket