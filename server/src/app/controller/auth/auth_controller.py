from pydantic import EmailStr
from sqlalchemy import select

from app.core.database import DB
from app.core.database_errors import (
	DatabaseConstraint,
)
from app.core.exception import APIException, ErrorMessage
from app.core.security import hash_password, verify_password
from app.models.user import User, UserConstraints
from app.schema.auth import RegisterRequest
from app.core.decorators import basic_api_guard,db_constraints_guard

# Controller methods focus solely on business logic.
#
# Cross-cutting concerns such as:
#   - transaction rollback
#   - IntegrityError handling
#   - database constraint resolution
#   - unexpected exception handling
#   - conversion to standardized APIException responses
#
# are delegated to decorators.
#
# Decorator usage:
#   - @basic_api_guard:
#       Preserves explicit APIException instances and converts
#       unexpected exceptions into InternalServerError responses.
#       Can optionally perform database rollbacks.
#
#   - @db_constraints_guard:
#       Extends basic_api_guard behavior by additionally converting
#       database IntegrityError exceptions into mapped API exceptions
#       using DatabaseConstraint definitions.
#
# This keeps controller methods focused on business rules while
# centralizing error handling logic in one place.


class AuthController:
	USER_CONSTRAINT_ERRORS = [
		DatabaseConstraint(
			constraint_name=UserConstraints.EMAIL_UQ.value,
			sqlite_identifier="users.email",
			message=ErrorMessage.EMAIL_ALREADY_EXISTS,
			exception=APIException.Conflict,
		),
		DatabaseConstraint(
			constraint_name=UserConstraints.USERNAME_UQ.value,
			sqlite_identifier="users.username",
			message=ErrorMessage.USERNAME_ALREADY_EXISTS,
			exception=APIException.Conflict,
		),
	]
	@staticmethod
	@basic_api_guard("An error occurred during the login process.")
	async def login(email: EmailStr, password: str, db: DB) -> User:
		"""
		Authenticate a user using their email and password.

		Returns:
			User: The authenticated user.

		Raises:
			APIException.Unauthorized:
				If the email does not exist or the password is incorrect.
			APIException.InternalServerError:
				If an unexpected error occurs during authentication.
		"""
		result = await db.execute(
			select(User).where(User.email == email)
		)
		user: User | None = result.scalar_one_or_none()

		if user is None:
			raise APIException.Unauthorized(
				ErrorMessage.INVALID_CREDENTIALS,
				debug_detail=(
					f"Login attempt failed for email: {email}. "
					"User not found."
				),
			)
		if not verify_password(password, user.hashed_password):
			raise APIException.Unauthorized(
				ErrorMessage.INVALID_CREDENTIALS,
				debug_detail=(
					f"Login attempt failed for email: {email}. "
					"Incorrect password."
				),
			)
		return user

	@staticmethod
	@db_constraints_guard(
		error_message="An error occurred during the registration process.",
		constraints=USER_CONSTRAINT_ERRORS,
	)
	async def register(data: RegisterRequest, db: DB) -> User:
		"""
		Register a new user.

		Returns:
			User: The newly created user.

		Raises:
			APIException.Conflict:
				If the username or email already exists.
			APIException.InternalServerError:
				If an unexpected error occurs during registration.
		"""
		new_user = User(
			email=data.email,
			full_name=data.full_name,
			role=data.role,
			username=data.username,
		)

		new_user.hashed_password = hash_password(data.password)

		db.add(new_user)

		await db.commit()
		await db.refresh(new_user)

		return new_user

	@staticmethod
	@basic_api_guard(
		"An error occurred while deleting the user.",
		rollback=True,
	)
	async def delete_user_by_id(user_id: int, db: DB) -> None:
		"""
		Delete a user by their ID.

		Raises:
			APIException.NotFound:
				If the user with the given ID does not exist.
			APIException.InternalServerError:
				If an unexpected error occurs during deletion.
		"""
		result = await db.execute(
			select(User).where(User.id == user_id)
		)
		user: User | None = result.scalar_one_or_none()

		if user is None:
			raise APIException.NotFound(
				ErrorMessage.USER_NOT_FOUND,
				debug_detail=(
					f"Deletion attempt failed for user_id: {user_id}. "
					"User not found."
				),
			)

		await db.delete(user)
		await db.commit()