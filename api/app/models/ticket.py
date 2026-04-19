from api.app.database import Mapped, mapped_column, String, ForeignKey, relationship, Base
from sqlalchemy import DateTime
from datetime import datetime, timezone


class Ticket(Base):
	__tablename__ = 'tickets'
	id: Mapped['int'] = mapped_column(primary_key=True)
	status: Mapped['str'] = mapped_column(String(20))
	description: Mapped['str'] = mapped_column(String(100))
	user_id: Mapped['int'] = mapped_column(ForeignKey('users.id'))
	created_at: Mapped['datetime'] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	user: Mapped['User'] = relationship(back_populates='tickets')

	def __repr__(self):
		return f"Ticker(id={self.id}, status={self.status})"