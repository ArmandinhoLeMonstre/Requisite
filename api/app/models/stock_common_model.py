from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class StockCommon(Base):
	__tablename__ = 'stock_common'
	id: Mapped['int'] = mapped_column(primary_key=True)
	title: Mapped['str'] = mapped_column(String(150))
	object_type: Mapped['str'] = mapped_column(String(20))
	object_specs: Mapped['str'] = mapped_column(String(100))
	quantity: Mapped['int'] = mapped_column()

	def __repr__(self):
		return f"Stock(id={self.id}, title={self.title}, object_type={self.object_type}, object_specs={self.object_specs}, quantity={self.quantity})"