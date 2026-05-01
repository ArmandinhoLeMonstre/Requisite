from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
import uuid

class InputList(Base):
	__tablename__ = "input_list"

	id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
	data: Mapped[dict] = mapped_column(JSONB)
