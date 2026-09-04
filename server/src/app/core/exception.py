from __future__ import annotations
from fastapi import HTTPException
from fastapi import status as http_status

from app.settings import settings

class ErrorMessage:
	"""
	Centralized repository for application error messages.

	Keeping error messages in a single location ensures consistency across
	the codebase and simplifies maintenance. Message updates can be made
	in one place without searching through controllers, services, or other
	application layers.

	This approach also reduces duplication, improves readability, and
	makes future localization or customization easier.
	"""

	# -----------------------------------------------------
	# AUTHENTICATION / SESSION
	# -----------------------------------------------------
	INCORRECT_PASSWORD = "Incorrect password"
	INVALID_CREDENTIALS = "Invalid credentials"
	ACCESS_TOKEN_EXPIRED = "Access token expired"
	ACCESS_TOKEN_INVALID = "Access token invalid"
	REFRESH_TOKEN_EXPIRED = "Refresh token expired"
	REFRESH_TOKEN_INVALID = "Refresh token invalid"
	SESSION_BUSY = "Current session is busy"

	# -----------------------------------------------------
	# USER / ACCOUNT
	# -----------------------------------------------------
	USER_NOT_FOUND = "User not found"
	EMAIL_ALREADY_EXISTS = "Email already exists"
	USERNAME_ALREADY_EXISTS = "Username already exists"

	# -----------------------------------------------------
	# DATABASE / INFRASTRUCTURE
	# -----------------------------------------------------
	DATABASE_ERROR = "Database operation failed"
	SERVICE_UNAVAILABLE = "Service is temporarily unavailable. Please try again later."

	# -----------------------------------------------------
	# GENERIC / FALLBACK
	# -----------------------------------------------------
	UNEXPECTED_ERROR = "An unexpected error occurred. Please try again later."


	# Granting access to specific actions based on user roles
	GRANTING_PRIVILEGE_ROLE_ERROR = "Users with a base VIEWER account cannot be granted elevated project roles."

	@staticmethod
	def invalid_role(role_name: str) -> str:
		return f"Access denied: your role '{role_name}' does not have permission."

	@staticmethod
	def not_found(resource: str, value: str | int) -> str:
		return f"{resource} with identifier '{value}' does not exist."

	@staticmethod
	def field_required(field_name: str) -> str:
		return f"The field '{field_name}' is required."

	@staticmethod
	def referential_integrity(details: str = "") -> str:
		return f"Referential integrity violation: {details}".strip()

	@staticmethod
	def unique_constraint_violation(field_name: str) -> str:
		return f"Unique constraint violation: '{field_name}' already exists."

	@staticmethod
	def not_found_with_id(resource: str, resource_id: int) -> str:
		return f"{resource} with ID {resource_id} not found."
	
	@staticmethod 
	def no_permission(action:str,resource: str) -> str:
		return f"You do not have permission to {action} {resource}."

class APIException:
	# =========================================================
	# BASE EXCEPTION
	# =========================================================
	class Base(HTTPException):
		def __init__(self, status_code: int, message: str,debug_detail: str = None):
			payload = {"message": message}
			if debug_detail and settings.DEBUG:
				payload["debug_detail"] = debug_detail
			
			super().__init__(status_code=status_code, detail=payload)



	# =====================================================
	# 4xx EXCEPTIONS
	# =====================================================
	class BadRequest(Base):
		def __init__(self, message="Bad request", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_400_BAD_REQUEST, message=message, debug_detail=debug_detail)

	class Unauthorized(Base):
		def __init__(self, message="Unauthorized", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_401_UNAUTHORIZED, message=message, debug_detail=debug_detail)

	class Forbidden(Base):
		def __init__(self, message="Forbidden", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_403_FORBIDDEN, message=message, debug_detail=debug_detail)

	class NotFound(Base):
		def __init__(self, message="Not found", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_404_NOT_FOUND, message=message, debug_detail=debug_detail)

	class Conflict(Base):
		def __init__(self, message="Conflict", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_409_CONFLICT, message=message, debug_detail=debug_detail)

	class UnprocessableEntity(Base):
		def __init__(self, message="Unprocessable entity", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_422_UNPROCESSABLE_CONTENT, message=message, debug_detail=debug_detail)


	class AttributeError(Base):
		def __init__(self, message="Attribute error", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_400_BAD_REQUEST, message=message, debug_detail=debug_detail)
	
	class ValidationError(Base):
		def __init__(self, message="Validation error", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_400_BAD_REQUEST, message=message, debug_detail=debug_detail)


	# =====================================================
	# 5xx EXCEPTIONS
	# =====================================================
	class InternalServerError(Base):
		def __init__(self, message="Internal server error", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, debug_detail=debug_detail)

	class ServiceUnavailable(Base):
		def __init__(self, message="Service unavailable", debug_detail: str = None):
			super().__init__(status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE, message=message, debug_detail=debug_detail)

