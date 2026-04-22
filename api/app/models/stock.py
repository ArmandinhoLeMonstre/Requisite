from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Stock(Base):
	__tablename__ = 'stock'
	id: Mapped['int'] = mapped_column(primary_key=True)
	category: Mapped['str'] = mapped_column(String(20))
	product: Mapped['str'] = mapped_column(String(50))
	quantity: Mapped['int'] = mapped_column(default=0)
	price: Mapped['float'] = mapped_column(default=0)

	def __repr__(self):
		return f"Stock(id={self.id}, produc={self.product}, quantity={self.quantity})"