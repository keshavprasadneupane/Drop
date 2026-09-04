import logging
import sys
import traceback


class Logger:
	"""A wrapper around `logging.Logger` with a fallback to `stdout` print formatting.

	If an explicit `logging.Logger` instance is not passed, messages are formatted
	and printed to stdout. Accepts standard `%`-style formatting arguments and
	`exc_info=True` for exception stack traces.
	"""

	def __init__(self, logger: logging.Logger | None = None):
		"""Initialize the Logger wrapper.

		Args:
			logger: Optional `logging.Logger` instance. If None, defaults to `stdout` printing.
					Pass `logging.getLogger(__name__)` to route through standard Python logging.
		"""
		self._logger = logger  

	def _log_print(self, level: str, msg: object, *args, **kwargs):
		"""Format and print log messages to stdout, including optional stack traces."""
		# Handle string interpolation (e.g., %s) or fall back to appending tuple if formatting fails
		if args:
			try:
				formatted_msg = str(msg) % args
			except TypeError:
				formatted_msg = f"{msg} {args}"
		else:
			formatted_msg = str(msg)

		print(f"[{level}] {formatted_msg}")

		# Extract and print traceback if exc_info is enabled
		exc_info = kwargs.get("exc_info")
		if exc_info:
			if isinstance(exc_info, bool):
				exc_info = sys.exc_info()
			if exc_info and exc_info[0] is not None:
				traceback.print_exception(*exc_info)

	def debug(self, msg: object, *args, **kwargs):
		"""Log a DEBUG level message."""
		if self._logger:
			self._logger.debug(msg, *args, **kwargs)
		else:
			self._log_print("DEBUG", msg, *args, **kwargs)

	def info(self, msg: object, *args, **kwargs):
		"""Log an INFO level message."""
		if self._logger:
			self._logger.info(msg, *args, **kwargs)
		else:
			self._log_print("INFO", msg, *args, **kwargs)

	def warning(self, msg: object, *args, **kwargs):
		"""Log a WARNING level message."""
		if self._logger:
			self._logger.warning(msg, *args, **kwargs)
		else:
			self._log_print("WARNING", msg, *args, **kwargs)

	def error(self, msg: object, *args, **kwargs):
		"""Log an ERROR level message."""
		if self._logger:
			self._logger.error(msg, *args, **kwargs)
		else:
			self._log_print("ERROR", msg, *args, **kwargs)


# Fallback mode: Prints directly to stdout
logger = Logger(None)  

# Standard logging mode: Uncomment to delegate to Python's logging module
# logger = Logger(logging.getLogger(__name__))