from app.database import Base, engine, get_db
from app.models.user import User
from app.models.ticket import Ticket
from app.models.group import Group
from app.models.stock import Stock
from sqlalchemy.orm import Session
from sqlalchemy import select