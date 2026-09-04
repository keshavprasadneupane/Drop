from enum import Enum
from datetime import datetime
from typing import TYPE_CHECKING
from app.models.base import Base
from app.models.static_files import MimeType
from sqlalchemy import (
	Integer, ForeignKey, DateTime, func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:  # to avoid circular import issues, only import for type checking
	from app.models.product import Product
	from app.models.static_files import StaticFile


class ProductImageConstraintsName(Enum):
	"""
	Using an Enum for constraint names ensures consistency and avoids hardcoding strings throughout the codebase.
	Useful for Database Error Resolving, especially when handling unique constraint violations or foreign key errors.
	"""
	FK_PRODUCT_IMAGES_FILE_ID = "fk_product_images_file_id"
	FK_PRODUCT_IMAGES_PRODUCT_ID = "fk_product_images_product_id"


class ProductImage(Base):
	"""
	A association table that links products to their images. Each entry represents a relationship between a product and an image file.
	This table has a many-to-many relationship with both Product and StaticFile models.
	For this table the mime type must be image/* .
	"""
	__tablename__ = "product_images"

	file_id: Mapped[int] = mapped_column(
		Integer, 
		ForeignKey(
			"static_files.id", 
			name=ProductImageConstraintsName.FK_PRODUCT_IMAGES_FILE_ID.value, 
			ondelete="CASCADE"
		), 
		primary_key=True,
	)
	product_id: Mapped[int] = mapped_column(
		Integer, 
		ForeignKey(
			"products.id", 
			name=ProductImageConstraintsName.FK_PRODUCT_IMAGES_PRODUCT_ID.value, 
			ondelete="CASCADE"
		), 
		primary_key=True
	)
	
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	# Relationships
	file: Mapped["StaticFile"] = relationship(
		"StaticFile", back_populates="product_images"
	)
	product: Mapped["Product"] = relationship(
		"Product", back_populates="product_images"
	)

	@staticmethod
	def is_supported_image_type(type: str) -> bool:
		"""
		Check if the provided mime type is a supported image type.
		:param type: The mime type to check.
		:return: True if the mime type is a supported image type, False otherwise.
		"""
		return type in MimeType.G_IMAGES