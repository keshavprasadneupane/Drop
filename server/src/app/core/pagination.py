import math
from typing import Type, TypeVar
from sqlalchemy import select, func
from sqlalchemy.sql import Select
from app.core.database import DB
from app.core.exception import APIException
from app.schema.pagination import PaginatedItems

M = TypeVar("M")  # Generic type variable for SQLAlchemy database models


class PaginationHelper:
	"""A reusable core service to safely execute bounded database page queries.

	Consolidates repetitive pagination boilerplate (offset calculations, row
	counting, and metadata schema hydration) into a single, type-safe interface
	capable of parsing any arbitrary database entity or pre-where_expressioned dataset.
	"""

	@staticmethod
	async def paginate_query_async(
		model: Type[M],
		*,
		db: DB,
		current_page: int,
		page_size: int = 10,
		base_query: Select | None = None
	) -> PaginatedItems[M]:
		"""Paginates an operational SQLAlchemy query or raw table configuration.

		Args:
			model: The target SQLAlchemy model class (e.g., Project, User).
			db: The active, injected async database session adapter.
			current_page: Targeted page sequence index (1-based index).
			page_size: Maximum volume threshold of matching items allowed per page window.
			base_query: An optional pre-where_expressioned query instance. If left blank,
				the engine constructs a clean base select statement from the model.

		Returns:
			A generic PaginatedItem container fully populated with records and metadata.

		Raises:
			APIException.ValidationError: If current_page or page_size are out of valid bounds.
			APIException.InternalServerError: Will 100% throw an exception if the database session is not async or if the model
				is not a valid SQLAlchemy model.
		"""
		try:
			if page_size <= 0:
				raise APIException.ValidationError(
					message=f"page_size must be a positive integer, got {page_size}"
				)
			if current_page <= 0:
				raise APIException.ValidationError(
					message=f"current_page must be a positive integer, got {current_page}"
				)

			if base_query is None:
				base_query = select(model)

			# 1, find the total count of items matching the base query
			count_query = select(func.count()).select_from(base_query.subquery())
			count_result = await db.execute(count_query)
			total_count = count_result.scalar_one()

			# 2, calculate the total number of pages based on the total count and page size
			total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
			items: list[M] = []

			# 3, if the current page is within the valid range, fetch the items for that page
			# fetch only if there are items to fetch and the current page is valid
			# so this saves heavy queries when the current page is out of range
			if total_count > 0 and current_page <= total_pages:
				offset = (current_page - 1) * page_size
				paginated_query = base_query.offset(offset).limit(page_size)

				result = await db.execute(paginated_query)
				items = result.scalars().all()

			# 4, return a PaginatedItems instance with the fetched items and metadata
			# or an empty list if the current page is out of range
			return PaginatedItems[M].from_data(
				items=items,
				total_items=total_count,
				current_page=current_page,
				page_size=page_size
			)
	
		except APIException.Base as ve:
			raise ve
		except Exception as e:
			raise APIException.InternalServerError(
				message=f"An error occurred while paginating the query",
				debug_detail=f"{str(e)}"
			)
	
	@staticmethod
	def paginate_query_sync(
		model: Type[M],
		*,
		db: DB,
		current_page: int,
		page_size: int = 10,
		base_query: Select | None = None
	) -> PaginatedItems[M]:
		"""
		Synchronous version of paginate_query_async for non-async contexts.
		Allows for the same pagination logic to be applied in synchronous code paths.
		Args:
			model: The target SQLAlchemy model class (e.g., Project, User).
			db: The active, injected synchronous database session adapter.
			current_page: Targeted page sequence index (1-based index).
			page_size: Maximum volume threshold of matching items allowed per page window.
			base_query: An optional pre-where_expressioned query instance. If left blank,
				the engine constructs a clean base select statement from the model.
		Returns:
			A generic PaginatedItem container fully populated with records and metadata.
		Raises:
			APIException.ValidationError: If current_page or page_size are out of valid bounds.
			APIException.InternalServerError: Will 100% throw an exception if the database session is not synchronous or 
				if the model is not a valid SQLAlchemy model.
		"""
		try:

			if page_size <= 0:
				raise APIException.ValidationError(
					message=f"page_size must be a positive integer, got {page_size}"
				)
			if current_page <= 0:
				raise APIException.ValidationError(
					message=f"current_page must be a positive integer, got {current_page}"
				)

			if base_query is None:
				base_query = select(model)

			# 1, find the total count of items matching the base query
			count_query = select(func.count()).select_from(base_query.subquery())
			count_result = db.execute(count_query)
			total_count = count_result.scalar_one()

			# 2, calculate the total number of pages based on the total count and page size
			total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
			items: list[M] = []

			# 3, if the current page is within the valid range, fetch the items for that page
			# fetch only if there are items to fetch and the current page is valid
			# so this saves heavy queries when the current page is out of range
			if total_count > 0 and current_page <= total_pages:
				offset = (current_page - 1) * page_size
				paginated_query = base_query.offset(offset).limit(page_size)

				result = db.execute(paginated_query)
				items = result.scalars().all()

			# 4, return a PaginatedItem instance with the fetched items and metadata
			# or an empty list if the current page is out of range
			return PaginatedItems[M].from_data(
				items=items,
				total_items=total_count,
				current_page=current_page,
				page_size=page_size
			)
		except APIException.Base as ve:
			raise ve
		except Exception as e:
			raise APIException.InternalServerError(
				message=f"An error occurred while paginating the query",
				debug_detail=f"{str(e)}"
			)