from app.database import Mapped, mapped_column, ForeignKey, relationship, Base, String


class Group(Base):
	__tablename__ = "groups"
	id: Mapped['int'] = mapped_column(primary_key=True)
	code: Mapped['str'] = mapped_column(String(5))
	manager_id: Mapped['int'] = mapped_column(ForeignKey("users.id"))

	users: Mapped[list['User']] = relationship(back_populates='group', foreign_keys="[User.group_id]")

	def __repr__(self):
		return f"Group(id={self.id}, manager_id={self.manager_id})"