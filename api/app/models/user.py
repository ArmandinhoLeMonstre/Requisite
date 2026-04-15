from api.app.database import Mapped, mapped_column, String, ForeignKey, relationship, Optional, Base
from sqlalchemy import Enum as SAEnum
import enum


class UserRole(enum.Enum):
	employee = "employee"
	manager = "manager"

class User(Base):
	__tablename__ = 'users'
	id: Mapped['int'] = mapped_column(primary_key=True)
	name: Mapped['str'] = mapped_column(String(40))
	email: Mapped['str'] = mapped_column(String(50))
	role: Mapped['str'] = mapped_column(SAEnum(UserRole))
	hashed_password: Mapped['str'] = mapped_column(String(100))
	group_id: Mapped[Optional['int']] = mapped_column(ForeignKey("groups.id"))

	tickets: Mapped[list["Ticket"]] = relationship(back_populates='user')
	group: Mapped[Optional['Group']] = relationship(back_populates='users')

	def __repr__(self):
		return f"User(id={self.id}, name={self.name}, email={self.email})"
	