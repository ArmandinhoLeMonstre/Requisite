from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from app.models.user import User
from app.init_db import engine, select
from app.models.ticket import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import TicketCreate
from fastapi import HTTPException

def create_ticket(ticket: TicketCreate, db: Session):
	try:
		user = db.scalars(select(User).where(User.id == ticket.user_id)).one()
	except SQLAlchemyError:
		raise HTTPException(status_code=404, detail="User not found")
	
	if user.group_id is None:
		raise HTTPException(status_code=403, detail="User is not in a group")
	
	ticket_stmt = Ticket(
		status= ticket.status,
		description= ticket.description,
		user_id= ticket.user_id,
	)
	
	try:
		db.add(ticket_stmt)
		db.commit()
		db.refresh(ticket_stmt)
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return ticket_stmt


def select_ticket(ticket_id: uuid.UUID, db: Session):
	try:
		ticket = db.scalars(select(Ticket).where(Ticket.id == ticket_id)).one()
	except NoResultFound:
		raise HTTPException(status_code=404, detail="Ticket not found")
	except SQLAlchemyError:
		raise HTTPException(status_code=500, detail="Error with Database server")
	
	return ticket