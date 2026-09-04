from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import (
	Integer, String, ForeignKey, DateTime, TypeDecorator, UniqueConstraint,
	func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING: # to avoid circular import issues, only import User for type checking
	from app.models.user import User
	from app.models.product_image import ProductImage

class StaticFileConstraintsName(Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	And Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	This do creates a verbose and more boilerplate code, but it is a good practice for maintainability and clarity.
	"""
	UNIQUE_URL = "uq_static_files_url"
	FK_STATIC_FILES_USER_ID = "fk_static_files_user_id"



class MimeType(Enum):
	"""
	An Enum for common MIME types, useful for validating and categorizing uploaded files.
	You can expand this list based on your application's requirements.
	"""
	IMAGE_JPEG = "image/jpeg"
	IMAGE_PNG = "image/png"
	IMAGE_GIF = "image/gif"
	PDF = "application/pdf"


class MimeTypeString(TypeDecorator):
	"""Stores as plain VARCHAR in DB, converts to MimeType Enum in Python."""
	impl = String
	cache_ok = True

	def __init__(self, length=100, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.impl = String(length)

	def process_bind_param(self, value, dialect):
		if value is None:
			return None
		return value.value if isinstance(value, MimeType) else str(value)

	def process_result_value(self, value, dialect):
		if value is None:
			return None
		try:
			return MimeType(value)
		except ValueError:
			# or u can log a warning or rase an exception if the value is not a valid MimeType
			return None 


class StaticFile(Base):
	__tablename__ = "static_files"
	__table_args__ = (
		UniqueConstraint("url", name=StaticFileConstraintsName.UNIQUE_URL.value),
	)

	id:Mapped[int] = mapped_column(Integer, primary_key=True)

	user_id:Mapped[int] = mapped_column(Integer, ForeignKey(
		"users.id",name=StaticFileConstraintsName.FK_STATIC_FILES_USER_ID.value
		), nullable=False)
	
	name:Mapped[str] = mapped_column(String(255), nullable=False,)
	url:Mapped[str] = mapped_column(String(255), nullable=False,)
	mime_type:Mapped[MimeType] = mapped_column(MimeTypeString(100), nullable=False,)	
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

	# Relationships
	user:Mapped["User"] = relationship("User", back_populates="static_files")
	product_images:Mapped[list["ProductImage"]] = relationship("ProductImage", back_populates="file")
