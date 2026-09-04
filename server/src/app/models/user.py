from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
	Integer, String, Boolean, Text, ForeignKey, DateTime, UniqueConstraint,
	Table, func, Column, sql, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr
from app.models.base import Base

if TYPE_CHECKING: # to avoid circular import issues, only import StaticFile for type checking
	from app.models.static_files import StaticFile


class UserRole(str, Enum):
	"""
	A Example Role Enum for a User model, demonstrating how to define roles with
	  associated permissions and hierarchy levels.
	Update the roles and their hierarchy as needed for your application.
	"""
	SUPER = "super"
	ADMIN = "admin"
	DEVELOPER = "developer"
	READER = "reader" # this represents the base role with read-only access to the system


	@property
	def label(self) -> str:
		"""Returns a human-readable label for frontend display."""
		return self.name.replace("_", " ").title()

	@property
	def hierarchy_level(self) -> int:
		"""
		Maps each role to a numerical weight for easy clearance level evaluations.
		Higher number means greater authorization.
		"""
		weights = {
			UserRole.READER: 10,
			UserRole.DEVELOPER: 20,
			UserRole.ADMIN: 30,
			UserRole.SUPER: 40,
		}
		return weights[self]

	def has_clearance(self, required_role: "UserRole") -> bool:
		"""
		Checks if this role meets or exceeds the required permission level.
		
		Example:
			current_user.role.has_clearance(UserRole.DEVELOPER)
		"""
		return self.hierarchy_level >= required_role.hierarchy_level

	# --- Domain Specific Permission Helpers ---

	@property
	def can_create_admin(self) -> bool:
		"""Only SUPER roles are authorized to provision or promote administrative accounts."""
		return self == UserRole.SUPER

	@property
	def can_manage_users(self) -> bool:
		"""ADMIN and SUPER roles possess user management credentials."""
		return self.has_clearance(UserRole.ADMIN)

	@property
	def can_modify_tickets(self) -> bool:
		"""DEVELOPER level and up can open, modify, or delete issue tickets."""
		return self.has_clearance(UserRole.DEVELOPER)

	@property
	def is_read_only(self) -> bool:
		"""Base users are explicitly confined to read-only views across the application."""
		return self == UserRole.READER


class UserConstraints(Enum):
	# Unique constraints for the User model
	EMAIL_UQ ="uq_users_email"
	USERNAME_UQ = "uq_users_username"


class User(Base):
	__tablename__ = "users"
	__table_args__ = (
        UniqueConstraint(
            "email",
            name=UserConstraints.EMAIL_UQ.value,
        ),
        UniqueConstraint(
            "username",
            name=UserConstraints.USERNAME_UQ.value,
        ),
    )
	
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	email: Mapped[EmailStr] = mapped_column(String(255), nullable=False)
	username: Mapped[str] = mapped_column(String(50), nullable=False)
	full_name: Mapped[Optional[str]] = mapped_column(String(100))
	hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
	role: Mapped[UserRole] = mapped_column(String(50), nullable=False, default=UserRole.READER)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True)
	created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
	soft_deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

	# Relationships
	static_files: Mapped[List["StaticFile"]] = relationship("StaticFile", back_populates="user", cascade="all, delete-orphan")