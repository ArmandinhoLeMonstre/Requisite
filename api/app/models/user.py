from app.database import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import Enum as SAEnum
import enum


class UserRole(enum.Enum):
	employee = "employee"
	manager = "manager"

class User(Base):
	__tablename__ = 'users'
	id: Mapped['int'] = mapped_column(primary_key=True)
	name: Mapped['str'] = mapped_column(String(50), unique=True)
	email: Mapped['str'] = mapped_column(String(120), unique=True)
	role: Mapped['str'] = mapped_column(SAEnum(UserRole))
	hashed_password: Mapped['str'] = mapped_column(String(200))
	group_id: Mapped[Optional['int']] = mapped_column(ForeignKey("groups.id"))

	tickets: Mapped[list["Ticket"]] = relationship(back_populates='user')
	group: Mapped[Optional['Group']] = relationship(back_populates='users', foreign_keys=[group_id])
	groups: Mapped[list['Group']] = relationship(back_populates='manager', foreign_keys="[Group.manager_id]")

	def __repr__(self):
		return f"User(id={self.id}, name={self.name}, email={self.email})"
	