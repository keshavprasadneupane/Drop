from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from fastapi import HTTPException
from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError

from app.core.exception import APIException, ErrorMessage


@dataclass(frozen=True, slots=True)
class DatabaseConstraint:
	"""
	Maps a database constraint to an API exception.

	Two independent matching strategies are required because Postgres
	and SQLite expose constraint violation info completely differently:

	- PostgreSQL: the named constraint (e.g. "uq_users_email") is
	  available structurally via error.orig.diag.constraint_name.
	  This is exact and reliable.

	- SQLite: the driver never surfaces the constraint name, even if
	  one was explicitly assigned in the schema. It only returns a raw
	  string like "UNIQUE constraint failed: users.email" — referencing
	  the table.column, not the constraint. This is a SQLite/sqlite3
	  driver limitation, not something fixable from the SQLAlchemy side.

	List order matters as a tiebreaker for sqlite_identifier matches:
	first match in the list wins if multiple constraints could match
	the same db_error substring.

	Contract on `message`:
	This is the ONLY error text shown to the client when this constraint
	matches. It must never contain raw SQL, driver text, table/column
	internals, or anything from the original exception. The resolver
	passes the raw db_error string separately as `debug_detail`, which
	is itself stripped entirely in production (gated by settings.DEBUG
	inside CustomException). `message` and `debug_detail` must never
	be swapped or merged.
	"""
	constraint_name: str       # used for Postgres exact match
	sqlite_identifier: str     # e.g. "users.email" — used for SQLite substring match
	message: str               # user-facing only — see "Contract on `message`" above
	exception: type[HTTPException]


class DatabaseErrorResolver:
	"""
	Converts database exceptions into application-specific API exceptions.
	Designed to work uniformly across Postgres and SQLite (and by extension
	any DBAPIError-compatible backend), despite their differing error formats.

	Every exception returned here respects DatabaseConstraint's message
	contract: client-facing `message` is always either a constraint's own
	`message` field or a static generic string — never raw db_error text.
	Raw db_error only ever flows into `debug_detail`.
	"""

	@staticmethod
	def _get_pg_diag(error: Exception) -> Optional[object]:
		"""
		Safely extract the psycopg diagnostics object, if present.
		Returns None on SQLite or any driver without structured diagnostics.
		"""
		orig = getattr(error, "orig", None)
		return getattr(orig, "diag", None)

	@staticmethod
	def _match_constraint(
		constraints: list[DatabaseConstraint],
		*,
		constraint_name: Optional[str] = None,
		db_error: Optional[str] = None,
	) -> Optional[HTTPException]:
		"""
		Attempts to find a DatabaseConstraint matching either the Postgres
		constraint_name or, failing that, the SQLite-style db_error substring.

		On match: constraint.message (user-facing, author-defined) goes to
		the client; raw identifying detail goes to debug_detail only.
		"""
		for constraint in constraints:
			# Postgres path: exact constraint name match
			if constraint_name and constraint.constraint_name == constraint_name:
				return constraint.exception(
					constraint.message,
					debug_detail=f"Constraint violation: {constraint_name}",
				)

			# SQLite path: substring match against table.column
			if db_error and constraint.sqlite_identifier.lower() in db_error:
				return constraint.exception(
					constraint.message,
					debug_detail=db_error,
				)

		return None

	@staticmethod
	def resolve(
		*,
		error: Exception,
		constraints: Iterable[DatabaseConstraint] = (),
	) -> HTTPException:

		db_error: str = str(getattr(error, "orig", error)).lower()
		constraints = list(constraints)

		if isinstance(error, IntegrityError):

			diag = DatabaseErrorResolver._get_pg_diag(error)
			constraint_name = getattr(diag, "constraint_name", None) if diag else None
			column_name = getattr(diag, "column_name", None) if diag else None
			table_name = getattr(diag, "table_name", None) if diag else None

			# ---- Postgres: named constraint present ----
			if constraint_name:
				matched = DatabaseErrorResolver._match_constraint(
					constraints, constraint_name=constraint_name,
				)
				if matched:
					return matched

				# Unmatched constraint: no DatabaseConstraint.message exists
				# for it, so we fall back to a static generic message.
				# Never surface the raw constraint_name to the client.
				return APIException.Conflict(
					"A database constraint was violated",
					debug_detail=(
						f"Unmatched constraint '{constraint_name}' "
						f"on table '{table_name}'"
					),
				)

			# ---- Postgres: unnamed NOT NULL, column_name still available ----
			# No DatabaseConstraint involved here either — ErrorMsg.field_required
			# builds a clean, safe message from just the column name, not raw SQL.
			if column_name and "not null" in db_error:
				return APIException.UnprocessableEntity(
					ErrorMessage.field_required(column_name),
					debug_detail=db_error,
				)

			# ---- SQLite (or any driver with no diag object) ----
			matched = DatabaseErrorResolver._match_constraint(
				constraints, db_error=db_error,
			)
			if matched:
				return matched

			# Below: no DatabaseConstraint matched at all (unknown/unconfigured
			# constraint). All messages here are static and generic by design —
			# there is no constraint.message to draw from since nothing matched.

			if "not null constraint failed" in db_error:
				field = (
					db_error.split(":")[-1].strip()
					if ":" in db_error
					else "field"
				)
				return APIException.UnprocessableEntity(
					ErrorMessage.field_required(field),
					debug_detail=db_error,
				)

			if "unique constraint" in db_error or "unique failed" in db_error:
				return APIException.Conflict(
					"Duplicate value violates unique constraint",
					debug_detail=db_error,
				)

			if "foreign key constraint failed" in db_error:
				return APIException.Conflict(
					"A related record does not exist or cannot be removed",
					debug_detail=db_error,
				)

			return APIException.Conflict(
				"A database constraint was violated",
				debug_detail=db_error,
			)

		if isinstance(error, OperationalError):
			return APIException.ServiceUnavailable(
				ErrorMessage.SERVICE_UNAVAILABLE,
				debug_detail=db_error,
			)

		if isinstance(error, DBAPIError):
			return APIException.InternalServerError(
				ErrorMessage.DATABASE_ERROR,
				debug_detail=db_error,
			)

		return APIException.InternalServerError(
			ErrorMessage.UNEXPECTED_ERROR,
			debug_detail=str(error),
		)