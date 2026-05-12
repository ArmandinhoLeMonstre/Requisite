from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.user_model import User, UserRole
from app.models.ticket_model import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import TicketCreate
from app.services.chat_services import new_message, Sender

from app.logger import logger

async def create_ticket(current_user: User,  db: AsyncSession):
	if current_user.group_id is None and current_user.role != UserRole.manager:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not in a group")
	
	ticket_stmt = Ticket(
		status= TicketStatus.opened,
		user_id= current_user.id,
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
