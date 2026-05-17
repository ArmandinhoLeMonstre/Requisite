from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Stock(Base):
	__tablename__ = 'stock'
	id: Mapped['int'] = mapped_column(primary_key=True)
	title: Mapped['str'] = mapped_column(String(150))
	object_type: Mapped['str'] = mapped_column(String(20))
	object_specs: Mapped['str'] = mapped_column(String(100))
	quantity: Mapped['int'] = mapped_column()
	manager_id: Mapped['int'] = mapped_column(ForeignKey('users.id'))

	manager: Mapped['User'] = relationship(back_populates='stock', lazy="selectin")

	def __repr__(self):
		return f"Stock(id={self.id}, title={self.title}, object_type={self.object_type}, object_specs={self.object_specs}, quantity={self.quantity})"