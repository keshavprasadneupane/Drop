from __future__ import annotations
from datetime import datetime, timedelta, UTC
from typing import Optional, Annotated

import jwt
from pydantic import EmailStr, EmailStr, TypeAdapter, ValidationError  # From pyjwt
from app.core.exception import APIException
from app.models.user import UserRole
from argon2 import PasswordHasher  # From argon2-cffi

from argon2.exceptions import VerifyMismatchError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.settings import settings

# Initialize the modern Argon2 hasher
ph = PasswordHasher()

SECRET_KEY = settings.SECRET_KEY
REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS





class EmailOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
	"""
	A custom form class that extends FastAPI's OAuth2PasswordRequestForm to validate 
	the username as an email address.
	This ensures that the username provided during login is a valid email address.
	
	"""
	@property
	def validated_email(self) -> EmailStr:
		try:
			return TypeAdapter(EmailStr).validate_python(self.username)
		except ValidationError:
			raise APIException.UnprocessableEntity(
				"Invalid email format for field 'email'. Please provide a valid email address.")



FormData = Annotated[EmailOAuth2PasswordRequestForm, Depends()]


# OAuth2PasswordBearer is used to extract the token from the Authorization header.
oauth_scheme = OAuth2PasswordBearer(
	# This is for Swagger UI to know where to send the username and password for token generation.
	# Otherwise, it is not needed for the actual token validation/generation, as we 
	# will handle that explicitly in our login endpoint.
	tokenUrl="/api/auth/login",
	scopes={role.value: role.label for role in UserRole}
)


Token = Annotated[str, Depends(oauth_scheme)]

def hash_password(password: str) -> str:
	"""Hashes a plain-text password using Argon2id."""
	return ph.hash(password)


def verify_password(password: str, hashed_pw: str) -> bool:
	"""
	Verify a plain-text password against a stored Argon2 hash.

	Note:
		Pass the password exactly as entered by the user. Do NOT hash it
		beforehand; Argon2 handles the hashing and comparison internally.
	"""
	try:
		return ph.verify(hashed_pw, password)
	except VerifyMismatchError:
		return False


def create_access_token(user_id: int, expire_delta: Optional[timedelta] = None) -> str:
	"""Generates a signed JWT Access Token."""
	to_encode: dict = {"sub": str(user_id)}
	expire = datetime.now(UTC) + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
	to_encode.update({"exp": expire})
	
	# PyJWT expects the payload, key, and algorithm name directly
	return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: int, expire_delta: Optional[timedelta] = None) -> str:
	"""Generates a signed JWT Refresh Token."""
	to_encode: dict = {"sub": str(user_id)}
	expire = datetime.now(UTC) + (expire_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
	to_encode.update({"exp": expire})
	
	return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)