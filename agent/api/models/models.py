from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from api.database import Base

class InputList(Base):
	__tablename__ = "input_list"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	data: Mapped[str] = mapped_column(String)
