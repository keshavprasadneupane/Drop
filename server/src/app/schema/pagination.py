from pydantic import BaseModel, ConfigDict
from typing import List

class PaginatedItems[T](BaseModel):
	"""A generic container for paginated API responses.

	Wraps a chunk of data items alongside the necessary metadata required
	by client applications to render pagination controls.

	Type Parameters:
		T: The Pydantic schema or SQLAlchemy model class representing 
		   the data items being paginated.
	"""
	items: List[T]
	total_items: int
	current_page: int
	page_size: int
	total_pages: int
	message:str 
	model_config = ConfigDict(arbitrary_types_allowed=True)
	@classmethod
	def from_data(
		cls, items: List[T], total_items: int, current_page: int, page_size: int,
		message:str|None = None
	) -> "PaginatedItems[T]":
		"""Factory method to construct a PaginationItem instance with automated page math.
		Args:
			items: The list of data entities fetched for the current page slice.
			total_items: The total count of existing items matching the query criteria.
			current_page: The index of the current page requested (typically 1-based).
			page_size: The maximum number of items requested per page.
			message: An optional custom message for the pagination response.

		Returns:
			An instantiated PaginationItem object fully populated with metadata.
		"""

		total_pages = (total_items + page_size - 1) // page_size if page_size > 0 else 0
		
		generated_message = PaginatedItems._get_message(
			total_items=total_items,
			current_page=current_page,
			total_pages=total_pages,
			items_count=len(items),
			custom_message=message
		)

		return cls(
			items=items,
			total_items=total_items,
			current_page=current_page,
			page_size=page_size,
			total_pages=total_pages,
			message= generated_message
		)
	
	@staticmethod
	def _get_message(total_items:int, current_page:int, total_pages:int, items_count:int, custom_message:str|None = None) -> str:
		"""Generates a user-facing message based on pagination state.
		Args:
			total_items: The total count of items matching the query.
			current_page: The index of the current page requested.
			total_pages: The total number of pages available.
			items_count: The number of items returned in the current page slice.
			custom_message: An optional custom message to override default behavior.
			"""
		if total_items == 0:
			return "No items found matching the query criteria."
		elif current_page > total_pages:
			return f"Requested page {current_page} exceeds total pages {total_pages}. No items to display."
		else:
			return (
				custom_message
				if custom_message is not None
				else f"Page {current_page} of {total_pages}, displaying {items_count} items out of {total_items} total."
			)