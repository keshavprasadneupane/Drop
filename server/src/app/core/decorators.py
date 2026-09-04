from functools import wraps
from inspect import iscoroutinefunction, signature
from typing import Iterable
from sqlalchemy.exc import IntegrityError
from app.core.database_errors import DatabaseConstraint, DatabaseErrorResolver
from app.core.exception import APIException


def handle_api_errors(
	error_message: str = "An unexpected error occurred.",
	rollback: bool = False,
	db_param_name: str = "db",
):
	"""
	Catch unhandled exceptions at the API boundary and map them to standard APIExceptions.

	This decorator is best suited for read operations (GET logic) or simple business
	logic layers. It handles unexpected failures by turning them into clean InternalServerError
	responses, while allowing explicitly raised application exceptions to pass through.

	Note:
		For write operations that rely on database-level constraints (e.g., unique bounds, 
		foreign keys), prefer using `@handle_db_errors`. When using this decorator on 
		writes, manually validate business rules beforehand:
		
		>>> user = grab_user_by_email(email, db)
		>>> if user:
		>>>     raise APIException.Conflict("User with this email already exists.")

	Typical usage:
		>>> @handle_api_errors("An error occurred while retrieving the user.")
		>>> async def get_user(user_id: int, db: Session):
		>>>     return await service.get_user(user_id, db)

		>>> @handle_api_errors("An error occurred while deleting the user.", rollback=True)
		>>> async def delete_user(user_id: int, db: Session):
		>>>     return await service.delete_user(user_id, db)

	Args:
		error_message: The user-facing message used if an unexpected error occurs.
		rollback: If True, automatically rolls back the database session on failure.
		db_param_name: The name of the DB session parameter in the decorated function.

	Raises:
		APIException: The original explicit APIException or a wrapped InternalServerError.
	"""
	def decorator(func):

		def get_db(*args, **kwargs):
			try:
				bound = signature(func).bind_partial(*args, **kwargs)
				return bound.arguments.get(db_param_name)
			except Exception:
				return None

		@wraps(func)
		async def async_wrapper(*args, **kwargs):
			db = get_db(*args, **kwargs)
			try:
				return await func(*args, **kwargs)
			except APIException.Base:
				if rollback and db is not None:
					await db.rollback()
				raise
			except Exception as e:
				if rollback and db is not None:
					await db.rollback()
				raise APIException.InternalServerError(
					message=error_message,
					debug_detail=str(e),
				)

		@wraps(func)
		def sync_wrapper(*args, **kwargs):
			db = get_db(*args, **kwargs)
			try:
				return func(*args, **kwargs)
			except APIException.Base:
				if rollback and db is not None:
					db.rollback()
				raise
			except Exception as e:
				if rollback and db is not None:
					db.rollback()
				raise APIException.InternalServerError(
					message=error_message,
					debug_detail=str(e),
				)

		return async_wrapper if iscoroutinefunction(func) else sync_wrapper

	return decorator


def handle_db_errors(
	*,
	error_message: str = "An unexpected database error occurred.",
	constraints: Iterable[DatabaseConstraint] = (),
	rollback: bool = True,
	db_param_name: str = "db",
):
	"""
	Intercept database integrity violations and map them to structured API responses.

	Designed for mutation operations (CREATE, UPDATE, DELETE). This decorator catches 
	SQLAlchemy `IntegrityError` exceptions (such as unique, foreign key, or check constraint 
	failures) and passes them to the `DatabaseErrorResolver` to translate them into 
	specific, actionable HTTP exceptions.

	Typical usage:
		@handle_db_errors(error_message="Registration failed.")
		async def register(payload: UserRegisterSchema, db: Session):
			...

		@handle_db_errors(
			error_message="Registration failed.",
			constraints=USER_CONSTRAINT_ERRORS,
		)
		async def register_with_custom_constraints(payload: UserRegisterSchema, db: Session):
			...

	Args:
		error_message: Fallback user-facing message if an unhandled non-DB exception occurs.
		constraints: Optional distinct mappings to override default DB error resolution rules.
		rollback: If True, automatically rolls back the database session on failure.
		db_param_name: The name of the DB session parameter in the decorated function.

	Raises:
		APIException: A resolved constraint error, the original exception, or an InternalServerError.
	"""
	def decorator(func):
		func_signature = signature(func)
		constraints_list = list(constraints)

		def get_db(*args, **kwargs):
			bound = func_signature.bind_partial(*args, **kwargs)
			return bound.arguments.get(db_param_name)

		@wraps(func)
		async def async_wrapper(*args, **kwargs):
			db = get_db(*args, **kwargs)
			try:
				return await func(*args, **kwargs)
			except IntegrityError as e:
				if rollback and db is not None:
					await db.rollback()
				raise DatabaseErrorResolver.resolve(
					error=e,
					constraints=constraints_list,
				)
			except APIException.Base:
				if rollback and db is not None:
					await db.rollback()
				raise
			except Exception as e:
				if rollback and db is not None:
					await db.rollback()
				raise APIException.InternalServerError(
					message=error_message,
					debug_detail=str(e),
				)

		@wraps(func)
		def sync_wrapper(*args, **kwargs):
			db = get_db(*args, **kwargs)
			try:
				return func(*args, **kwargs)
			except IntegrityError as e:
				if rollback and db is not None:
					db.rollback()
				raise DatabaseErrorResolver.resolve(
					error=e,
					constraints=constraints_list,
				)
			except APIException.Base:
				if rollback and db is not None:
					db.rollback()
				raise
			except Exception as e:
				if rollback and db is not None:
					db.rollback()
				raise APIException.InternalServerError(
					message=error_message,
					debug_detail=str(e),
				)

		return async_wrapper if iscoroutinefunction(func) else sync_wrapper

	return decorator
