from __future__ import annotations

from typing import Annotated
from sqlalchemy import select
from fastapi import Security
from fastapi.security import SecurityScopes
import jwt

from server.core.database import DB
from server.core.exception import APIException, ErrorMsg
from server.core.security import Token, SECRET_KEY, ALGORITHM
from server.models import User
from server.models.user import UserRole


async def get_user_by_email(email_id: str, db: DB):
	result = await db.execute(select(User).where(User.email == email_id))
	return result.scalar_one_or_none()


async def get_current_user(
	security_scopes: SecurityScopes,
	token: Token,
	db: DB
) -> User:

	credentials_error = APIException.Unauthorized(ErrorMsg.INVALID_CREDENTIALS)

	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		user_id = payload.get("sub")

		if user_id is None:
			raise credentials_error

	except jwt.ExpiredSignatureError:
		raise APIException.Unauthorized(ErrorMsg.ACCESS_TOKEN_EXPIRED)

	except jwt.PyJWTError:
		raise APIException.Unauthorized(ErrorMsg.ACCESS_TOKEN_INVALID)

	user: User = await get_user_by_email(user_id, db)

	if not user:
		raise credentials_error

	if security_scopes.scopes:
		if user.role not in security_scopes.scopes:
			raise APIException.Forbidden(
				ErrorMsg.invalid_role(user.role)
			)

	return user


IsAdmin = Annotated[
	User,
	Security(get_current_user, scopes=[UserRole.ADMIN.value])
]

AnyUser = Annotated[
	User,
	Security(get_current_user)
]