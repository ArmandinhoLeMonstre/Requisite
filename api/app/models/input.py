from app.database import Mapped, mapped_column, Base, ForeignKey, String
from sqlalchemy import DateTime, Text
from datetime import datetime, timezone

class Input(Base):
	__tablename__ = 'inputs'
	id: Mapped['int'] = mapped_column(primary_key=True)
	message: Mapped['str'] = mapped_column(Text)
	ticket_id: Mapped['int'] = mapped_column(ForeignKey('tickets.id'))
	created_at: Mapped['datetime'] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

	def __repr__(self):
		return f"Input(id={self.id}, message={self.message}, ticket_id={self.ticket_id})"
