from functools import wraps
from inspect import iscoroutinefunction, signature
from sqlalchemy.exc import IntegrityError
from app.core.database_errors import DatabaseErrorResolver
from app.core.exception import APIException


def basic_api_guard(
	error_message: str,
	rollback: bool = False,
	db_param_name: str = "db",
	):
	"""
	Generic exception-handling decorator for controller and service methods.

	Used to eliminate repetitive try/except blocks when only standard
	API error handling is required.

	Best suited for read operations (GET-style logic), but can also be
	used for write operations when database constraint resolution is not
	needed. Optionally performs transaction rollback before propagating
	errors.

	Behavior:
		- Preserves explicitly raised APIException instances.
		- Converts unexpected exceptions into InternalServerError.
		- Supports both sync and async functions.
		- Optionally rolls back the database session on failure.

	Typical usage:

		@basic_api_guard(
			"An error occurred while retrieving the user."
		)
		async def get_user(...):
			...

		@basic_api_guard(
			"An error occurred while deleting the user.",
			rollback=True,
		)
		async def delete_user(...):
			...

	Args:
		error_message:
			User-facing message used when an unexpected exception occurs.

		rollback:
			Whether to automatically roll back the database session
			before re-raising exceptions.

		db_param_name:
			Name of the database session parameter in the decorated
			function signature.

	Raises:
		APIException:
			The original APIException or a generated
			InternalServerError.
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

		return (
			async_wrapper
			if iscoroutinefunction(func)
			else sync_wrapper
		)

	return decorator



def db_constraints_guard(
	*,
	error_message: str,
	constraints: list,
	rollback: bool = True,
	db_param_name: str = "db",
):
	"""
	Database-aware exception-handling decorator for create, update,
	and delete operations.

	Used when a method may trigger database constraint violations such as
	UNIQUE, FOREIGN KEY, CHECK, or NOT NULL constraints.

	This decorator removes the need for repetitive IntegrityError,
	rollback, and generic exception handling code by automatically
	translating database constraint failures into structured API
	exceptions.

	Behavior:
		- Resolves IntegrityError exceptions using
		DatabaseErrorResolver.
		- Preserves explicitly raised APIException instances.
		- Converts unexpected exceptions into InternalServerError.
		- Supports both sync and async functions.
		- Automatically rolls back failed transactions when enabled.

	Typical usage:

		@db_constraints_guard(
			error_message="Registration failed.",
			constraints=USER_CONSTRAINT_ERRORS,
		)
		async def register(...):
			...

		@db_constraints_guard(
			error_message="Failed to create project.",
			constraints=PROJECT_CONSTRAINT_ERRORS,
		)
		async def create_project(...):
			...

	Args:
		error_message:
			User-facing message used when an unexpected exception occurs.

		constraints:
			Collection of DatabaseConstraint mappings used to convert
			database constraint violations into API exceptions.

		rollback:
			Whether to automatically roll back the database session
			before re-raising exceptions.

		db_param_name:
			Name of the database session parameter in the decorated
			function signature.

	Raises:
		APIException:
			A constraint-specific API exception resolved from an
			IntegrityError, the original APIException, or a generated
			InternalServerError.
	"""

	def decorator(func):
		func_signature = signature(func)

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
					constraints=constraints,
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
					constraints=constraints,
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

		return (
			async_wrapper
			if iscoroutinefunction(func)
			else sync_wrapper
		)

	return decorator