from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.init_db import engine, select
from app.models.ticket import TicketStatus, Ticket, uuid
from app.schemas.ticket_schemas import RequestTicket
from fastapi import HTTPException

def create_ticket(ticket: RequestTicket):
	with Session(engine) as session:
		ticket_stmt = Ticket(
			status= ticket.status,
			description= ticket.description,
			user_id= ticket.user_id,
		)
		try:
			user = session.scalars(select(User).where(User.id == ticket.user_id)).one()
			user.tickets.append(ticket_stmt)
		except SQLAlchemyError:
			raise HTTPException(status_code=404, detail="User not found")
		try:
			session.add(ticket_stmt)
			session.commit()
		except SQLAlchemyError:
			raise HTTPException(status_code=500, detail="Error with Database server")
		session.refresh(ticket_stmt)
		return ticket_stmt


def select_ticket(ticket_id: uuid.UUID):
	with Session(engine) as session:
		try:
			ticket = session.scalars(select(Ticket).where(Ticket.id == ticket_id)).one()
		except SQLAlchemyError:
			raise HTTPException(status_code=404, detail="Ticket not found")
		return ticket