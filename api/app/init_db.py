from app.database import Base, engine
from app.models.user import User
from app.models.ticket import Ticket
from app.models.group import Group
from app.models.input import Input
from app.models.stock import Stock

Base.metadata.create_all(engine)