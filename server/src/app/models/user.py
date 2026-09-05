from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, List, Optional
from app.core.database import DB


from sqlalchemy import (
	Integer, String, Boolean, Text, ForeignKey, DateTime, UniqueConstraint,
	Table, func, Column, sql, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr
from app.models.base import Base

if TYPE_CHECKING: # to avoid circular import issues, only import StaticFile for type checking
	from app.models.static_files import StaticFile
	from app.models.product import Product

class UserRole(str, Enum):
	"""
	A Example Role Enum for a User model, demonstrating how to define roles with
	  associated permissions and hierarchy levels.
	Update the roles and their hierarchy as needed for your application.
	"""
	SUPER = "super"
	ADMIN = "admin"
	LISTER = "lister" # this represents a user with the ability to list and view items
	CUSTOMER = "customer" # this represents a user with the ability to make purchases


	@property
	def label(self) -> str:
		"""Returns a human-readable label for frontend display."""
		return self.name.replace("_", " ").title()

	def has_clearance(self, required_role: "UserRole") -> bool:
		"""
		Checks if the current role has clearance for the required role.
		:param required_role: The role to check against.
		:return: True if the current role has clearance, False otherwise.
		"""
		return self == required_role
	

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
	role: Mapped[str] = mapped_column(String(50), nullable=False, default=UserRole.CUSTOMER)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True)
	created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
	soft_deleted_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)

	# Relationships
	static_files: Mapped[List["StaticFile"]] = relationship("StaticFile", back_populates="user", cascade="all, delete-orphan")
	products: Mapped[List["Product"]] = relationship("Product", back_populates="user", cascade="all, delete-orphan")