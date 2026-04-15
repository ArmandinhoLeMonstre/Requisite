from api.app.database import Base, engine
from api.app.models.user import User
from api.app.models.ticket import Ticket
from api.app.models.group import Group
from api.app.models.input import Input
from api.app.models.stock import Stock

Base.metadata.create_all(engine)