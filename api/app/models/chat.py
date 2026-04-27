from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Text, ForeignKey, Uuid
from datetime import datetime, UTC
from sqlalchemy import Enum as SAEnum
import enum
import uuid


class Sender(enum.Enum):
	User = "user"
	agent = "agent"

class Chat(Base):
	__tablename__ = 'inputs'
	id: Mapped['int'] = mapped_column(primary_key=True)
	ticket_id: Mapped['uuid.UUID'] = mapped_column(ForeignKey('tickets.id'))
	sender: Mapped['str'] = mapped_column(SAEnum(Sender))
	message: Mapped['str'] = mapped_column(Text)
	created_at: Mapped['datetime'] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

	ticket: Mapped['Ticket'] = relationship(back_populates='chats', foreign_keys=[ticket_id])

	def __repr__(self):
		return f"Input(id={self.id}, message={self.message}, ticket_id={self.ticket_id})"
