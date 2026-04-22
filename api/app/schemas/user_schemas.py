from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import UserRole
from typing import Optional
from app.schemas.ticket_schemas import TicketResponse


class UserBase(BaseModel):
	name: str = Field(min_length=1, max_length=50)
	email: EmailStr = Field(max_length=120)
	role: UserRole
	group_id: Optional[int] = None


class UserCreate(UserBase):
	hashed_password: str


class UserResponse(UserBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	tickets: list[TicketResponse]
	