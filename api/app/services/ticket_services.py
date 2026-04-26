from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from fastapi import HTTPException, status

from app.init_db import engine, select

from app.models.user import User
from app.models.ticket import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import TicketCreate


def create_ticket(ticket: TicketCreate, user: User,  db: Session):
	if user.group_id is None:
		raise HTTPException(status_code=403, detail="User is not in a group")
	
	ticket_stmt = Ticket(
		status= ticket.status,
		description= ticket.description,
		user_id= user.id,
	)
	
	try:
		db.add(ticket_stmt)
		db.commit()
		db.refresh(ticket_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return ticket_stmt


def select_ticket(ticket_id: uuid.UUID, user: User, db: Session):
	try:
		ticket = db.scalars(select(Ticket).where(Ticket.id == ticket_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	if user.id != ticket.user_id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Not authorized to see this ticket"
		)
	
	return ticket