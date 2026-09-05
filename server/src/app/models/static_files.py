from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import (
	Integer, String, ForeignKey, DateTime, UniqueConstraint,
	func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING: # to avoid circular import issues, only import User for type checking
	from app.models.user import User
	from app.models.product_image import ProductImage

class StaticFileConstraintsName(str,Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	And Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	This do creates a verbose and more boilerplate code, but it is a good practice for maintainability and clarity.
	"""
	UNIQUE_URL = "uq_static_files_url"
	FK_STATIC_FILES_USER_ID = "fk_static_files_user_id"


class MimeType(str, Enum):
    """Enumeration for common MIME types and grouped validation helpers.

    Inherits from `str` and `Enum` to allow seamless string comparisons and 
    automatic JSON serialization in API response frameworks like FastAPI/Pydantic.

    Attributes:
        IMAGE_*: Supported image MIME type constants.
        PDF: Application PDF constant.
    """

    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_GIF = "image/gif"
    IMAGE_BMP = "image/bmp"
    IMAGE_WEBP = "image/webp"

    PDF = "application/pdf"

class MineTypeEnumGroup:
	"""
	Groupings of MIME types for validation and categorization.
	Attributes:
		G_IMAGES: List of all supported image MIME types for file validation.
		G_APPLICATIONS: List of all supported application MIME types.
		G_ALL: Consolidated list of all registered MIME types.
	"""
	G_IMAGES = [MimeType.IMAGE_JPEG, MimeType.IMAGE_PNG, MimeType.IMAGE_GIF, MimeType.IMAGE_BMP, MimeType.IMAGE_WEBP]
	G_APPLICATIONS = [MimeType.PDF]
	G_ALL = G_IMAGES + G_APPLICATIONS


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
	mime_type:Mapped[str] = mapped_column(String(100), nullable=False,)	
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

	# Relationships
	user:Mapped["User"] = relationship("User", back_populates="static_files")
	product_images:Mapped[list["ProductImage"]] = relationship("ProductImage", back_populates="file")
