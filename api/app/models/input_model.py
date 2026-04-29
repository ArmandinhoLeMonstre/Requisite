from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base

class InputList(Base):
	__tablename__ = "input_list"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	data: Mapped[dict] = mapped_column(JSONB)
