from app.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Uuid
from datetime import datetime, UTC
from sqlalchemy import Enum as SAEnum
import enum
import uuid

class TicketStatus(enum.Enum):
	pending= "pending"
	approved= "approved"
	rejected= "rejected"


class Ticket(Base):
	__tablename__ = 'tickets'
	id: Mapped['uuid.UUID'] = mapped_column(Uuid, primary_key=True, default= uuid.uuid4)
	status: Mapped['str'] = mapped_column(SAEnum(TicketStatus), nullable=True)
	description: Mapped['str'] = mapped_column(String(200), nullable=True)
	user_id: Mapped['int'] = mapped_column(ForeignKey('users.id'))
	created_at: Mapped['datetime'] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

	user: Mapped['User'] = relationship(back_populates='tickets', lazy="selectin")
	chats: Mapped[list['Chat']] = relationship(back_populates='ticket', foreign_keys="[Chat.ticket_id]", order_by="Chat.created_at", lazy="selectin")

	def __repr__(self):
		return f"Ticket(id={self.id}, status={self.status})"