from pydantic import BaseModel, ConfigDict
from app.models.user import UserRole


class UserBase(BaseModel):
	name: str
	email: str
	role: UserRole
	group_id: int | None = None

class RequestUser(UserBase):
	hashed_password: str

class ResponseUser(UserBase):
	model_config = ConfigDict(from_attributes=True)

	id: int