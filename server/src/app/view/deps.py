from __future__ import annotations

from typing import Annotated, Optional
from fastapi import Security, Depends
from fastapi.security import SecurityScopes
import jwt

from app.core.database import DB
from app.core.exception import APIException, ErrorMessage
from app.core.security import Token, decode_access_token, oauth_scheme_optional
from app.models import User
from app.models.user import UserRole 


async def get_current_user(
	security_scopes: SecurityScopes,
	token: Token,
	db: DB
) -> User:
	credentials_error = APIException.Unauthorized(ErrorMessage.INVALID_CREDENTIALS)

	try:
		payload = decode_access_token(token)
		user_id = payload.get("sub")
		if user_id is None:
			raise credentials_error
	except jwt.ExpiredSignatureError:
		raise APIException.Unauthorized(ErrorMessage.ACCESS_TOKEN_EXPIRED)
	except jwt.PyJWTError:
		raise APIException.Unauthorized(ErrorMessage.ACCESS_TOKEN_INVALID)

	user: User = await db.get(User, int(user_id))
	if not user:
		raise credentials_error

	if security_scopes.scopes:
		try:
			current_user_role = UserRole(user.role)
		except ValueError:
			raise APIException.Forbidden(ErrorMessage.invalid_role(user.role))
		has_access = False
		for scope_str in security_scopes.scopes:
			try:
				required_role = UserRole(scope_str)
				if current_user_role.has_clearance(required_role):
					has_access = True
					break
			except ValueError:
				continue 

		if not has_access:
			raise APIException.Forbidden(
				ErrorMessage.invalid_role(user.role)
			)

	return user


# --- Optional User Function for Public/Private Routes ---

async def get_optional_user(
	db: DB,
	# Targets the companion scheme so unauthenticated browsers pass through cleanly
	token: Optional[str] = Depends(oauth_scheme_optional)
) -> User | None:
	"""
	Attempts to parse the authentication token. 
	If a valid token is present, returns the User object.
	If the token is missing, expired, or invalid, returns None without raising an error.
	"""
	if not token:
		return None
		
	try:
		payload = decode_access_token(token)
		user_id = payload.get("sub")
		if user_id is None:
			return None
			
		user = await db.get(User, int(user_id))
		return user
		
	except (jwt.PyJWTError, ValueError):
		return None


SuperUser = Annotated[
	User,
	Security(get_current_user, scopes=[UserRole.SUPER.value])
]

AdminUser = Annotated[
	User,
	Security(get_current_user, scopes=[UserRole.ADMIN.value])
]

ListerUser = Annotated[
	User,
	Security(get_current_user, scopes=[UserRole.LISTER.value])
]

# Reader or any authenticated user can hit these routes
CustomerUser = Annotated[
	User,
	Security(get_current_user, scopes=[UserRole.CUSTOMER.value])
]

AuthenticatedUser = Annotated[
	User,
	# so any authenticated user can hit these routes, regardless of role
	# for now scoping to Customer and Lister roles, but can be expanded to include other roles as needed
	Security(get_current_user, scopes=[UserRole.CUSTOMER.value, UserRole.LISTER.value])
]

OpenUser = Annotated[
	Optional[User],
	Depends(get_optional_user)
]