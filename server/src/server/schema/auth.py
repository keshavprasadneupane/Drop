from typing import Optional

from pydantic import BaseModel, EmailStr

from server.models.user import UserRole

class LoginResponse(BaseModel):
	user_id: int
	role: str
	access_token: str
	refresh_token: str
	token_type: str


class RegisterRequest(BaseModel):
	email: EmailStr
	password: str
	username: str
	full_name: str
	role:Optional[str] = UserRole.READER.value


class RegisterResponse(BaseModel):
	user_id: int
	message: str

class MeResponse(BaseModel):
	"""
	THis model only gives very basic information about user,
	so frondend can use this to constomize the UI based on user role and other information.
	"""
	user_id: int
	username: str
	role: str