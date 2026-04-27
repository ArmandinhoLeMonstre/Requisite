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
	password: str = Field(min_length=4)


class UserUpdate(UserBase):
	model_config = ConfigDict(from_attributes=True, )

	name: str | None = Field(default=None, min_length=1, max_length=50)
	email: EmailStr | None = Field(default=None, max_length=120)
	role: UserRole | None = Field(default=None)
	group_id: int | None = Field(default=None)


class UserPublic(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	name: str
	role: UserRole
	group_id: int | None = None
	tickets: list[TicketResponse]


class UserPrivate(UserPublic):
	email: EmailStr


class Token(BaseModel):
	access_token: str
	tocket_type: str	
