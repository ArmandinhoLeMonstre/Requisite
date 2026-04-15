from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, DeclarativeBase
from typing import Optional


sqlite_url = f"sqlite:///sqlite.db"

engine = create_engine(sqlite_url, echo=True)

class Base(DeclarativeBase):
	pass