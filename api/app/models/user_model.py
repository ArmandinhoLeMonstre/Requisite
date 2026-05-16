from app.database import Base
from sqlalchemy import String, ForeignKey, Boolean
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
	email_verified: Mapped['bool'] = mapped_column(Boolean, default=False)
	email_verification_token: Mapped[Optional['str']] = mapped_column(String(100), nullable=True)

	tickets: Mapped[list["Ticket"]] = relationship(back_populates='user', lazy="selectin")
	group: Mapped[Optional['Group']] = relationship(back_populates='users', foreign_keys=[group_id], lazy="selectin")
	groups: Mapped[list['Group']] = relationship(back_populates='manager', foreign_keys="[Group.manager_id]", lazy="selectin")

	def __repr__(self):
		return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role})"
	