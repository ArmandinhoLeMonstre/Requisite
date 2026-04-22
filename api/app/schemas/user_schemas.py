from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import UserRole


class UserBase(BaseModel):
	name: str = Field(min_length=1, max_length=50)
	email: EmailStr = Field(max_length=120)
	role: UserRole
	group_id: int | None = None

class RequestUser(UserBase):
	hashed_password: str

class ResponseUser(UserBase):
	model_config = ConfigDict(from_attributes=True)

	id: int