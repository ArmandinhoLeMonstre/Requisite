from app.database import Mapped, mapped_column, String, ForeignKey, relationship, Base
from sqlalchemy import DateTime, Uuid
from datetime import datetime, timezone
from sqlalchemy import Enum as SAEnum
import enum
import uuid

class TicketStatus(enum.Enum):
	completed= "completed"
	opened= "opened"
	waiting_for_approval= "waiting_for_approval"
	approved= "approved"
	refused= "refused"


class Ticket(Base):
	__tablename__ = 'tickets'
	id: Mapped['uuid.UUID'] = mapped_column(Uuid, primary_key=True, default= uuid.uuid4)
	status: Mapped['str'] = mapped_column(SAEnum(TicketStatus))
	description: Mapped['str'] = mapped_column(String(100))
	user_id: Mapped['int'] = mapped_column(ForeignKey('users.id'))
	created_at: Mapped['datetime'] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	user: Mapped['User'] = relationship(back_populates='tickets')

	def __repr__(self):
		return f"Ticket(id={self.id}, status={self.status})"