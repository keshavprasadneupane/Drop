from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Iterable

from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError

from app.core.exception import APIException, ErrorMessage


@dataclass(frozen=True, slots=True)
class DatabaseConstraint:
	"""
	Overrides the auto-detected message/exception for a specific
	constraint.

	This is OPTIONAL. Unique, foreign-key, not-null, check, exclusion,
	and primary-key violations are already classified automatically on
	both backends (see _PG_SQLSTATE_MAP / _SQLITE_ERRORNAME_MAP). Only
	add a DatabaseConstraint when a particular constraint needs a
	message or exception type different from the generic auto-detected
	one (e.g. "This email is already registered" instead of the
	generic "A unique value already exists").

	Two matching strategies are required because database backends
	expose constraint information differently:

	PostgreSQL
	------------
	Matched by exact constraint_name. Populated the same way whether
	the underlying driver is psycopg (via diag.constraint_name) or
	asyncpg (via the attribute directly on the driver exception) —
	see _get_pg_diagnostics.

	SQLite
	--------
	Does not expose named constraints, so matching falls back to
	searching for a configured table.column identifier within the
	raw error text.
	"""

	constraint_name: str
	sqlite_identifier: str
	message: str
	exception: type[APIException.Base]


class DatabaseErrorResolver:
	"""
	Translates low-level database exceptions into application-specific
	API exceptions.

	Resolution order:

	1. Explicit DatabaseConstraint match (constraint_name for
	   PostgreSQL, sqlite_identifier substring for SQLite) — used when
	   you want a specific, custom-worded response for a particular
	   constraint.
	2. Automatic classification via a driver-provided error code,
	   which doesn't depend on constraint naming or message wording:
	   - PostgreSQL: the SQLSTATE code, standardized across all
	     constraint types and available identically on both driver
	     families this resolver supports:
	       * psycopg (sync, `postgresql+psycopg2` /
	         `postgresql+psycopg`): exposed as `orig.diag.sqlstate`,
	         with column/field names lifted out of
	         `diag.message_detail`'s "Key (col)=(val) ..." format for
	         unique, foreign-key, and exclusion violations, straight
	         from `diag.column_name` for not-null violations, and
	         from `diag.constraint_name` for check violations (which
	         have no reliable Key(...)= detail to parse).
	       * asyncpg (async, `postgresql+asyncpg`): the real
	         `asyncpg.exceptions.PostgresError` carries `sqlstate`,
	         `constraint_name`, `column_name`, `table_name`, and
	         `detail` as flat attributes (no `diag`-style wrapper like
	         psycopg has). The catch: SQLAlchemy's asyncpg dialect
	         wraps that real exception in its own thin
	         `AsyncAdapt_asyncpg_dbapi.Error`, and `error.orig` is
	         *that wrapper*, not the real asyncpg exception — the
	         wrapper only forwards `pgcode`/`sqlstate`, so
	         `orig.constraint_name` etc. are always None. The real
	         exception must be unwrapped first, via
	         `orig.driver_exception` (SQLAlchemy 2.1+) or
	         `orig.__cause__` (older SQLAlchemy) — see
	         `_get_pg_diagnostics` for the full unwrap logic. Once
	         unwrapped, column/field names are extracted the same way
	         as psycopg: from `detail`'s "Key (col)=(val) ..." format
	         for unique/FK/exclusion violations, from `column_name`
	         directly for not-null violations, and from
	         `constraint_name` for check violations.
	     Both shapes are normalized into one internal representation
	     (`_PgDiagnostics`) before classification, so the SQLSTATE
	     lookup table and extraction logic only need to be written
	     once.
	   - SQLite: the extended result code name (`sqlite_errorname`,
	     e.g. "SQLITE_CONSTRAINT_UNIQUE"; requires Python 3.11+), with
	     column names parsed from the "constraint failed: table.col"
	     tail for unique / primary-key / not-null violations.
	3. Text-pattern fallback (SQLite only, when `sqlite_errorname`
	   isn't available) by scanning the raw error message.
	4. Generic fallback (APIException.Conflict / InternalServerError)
	   for anything unrecognized, plus infrastructure-level failures
	   (OperationalError, bare DBAPIError) that aren't constraint
	   violations at all.

	Passing `constraints` is entirely optional — step 2 already covers
	unique / foreign-key / not-null / check / exclusion / primary-key
	violations out of the box on both backends, with as much
	specificity as each backend's error format actually supports.
	"""

	FALLBACK_CONSTRAINT_MESSAGE = (
		"[UNCLASSIFIED CONSTRAINT] Constraint violation could not be "
		"classified via SQLSTATE or text matching. "
	)

	# SQLSTATE class 23 = "integrity constraint violation".
	# https://www.postgresql.org/docs/current/errcodes-appendix.html
	_PG_SQLSTATE_MAP: dict[str, tuple[type[APIException.Base], str]] = {
		"23505": (APIException.Conflict, "A unique value already exists"),
		"23503": (APIException.Conflict, "A referenced record does not exist"),
		"23502": (APIException.UnprocessableEntity, "A required field is missing"),
		"23514": (APIException.UnprocessableEntity, "A check constraint was violated"),
		"23P01": (APIException.Conflict, "Conflicting record exists"),
	}

	# SQLSTATEs whose message_detail reliably follows Postgres's
	# standard "Key (col1, col2)=(val1, val2) ..." format, verified
	# against Postgres's own documented examples:
	#   unique_violation:      "Key (email)=(a@x.com) already exists."
	#   foreign_key_violation: "Key (org_id)=(999) is not present in table \"orgs\"."
	#   exclusion_violation:   "Key (room_id, during)=(1, [...)) conflicts
	#                            with existing key (room_id, during)=(1, [...))."
	#                            — same "Key (...)=..." prefix, so the
	#                            existing _PG_KEY_COLUMN_PATTERN matches
	#                            it without any changes.
	# This format is identical for psycopg's diag.message_detail and
	# asyncpg's exception.detail, since both are just surfacing the
	# server's DETAIL field verbatim.
	# check_violation (23514) is deliberately excluded: its detail
	# (when present at all) is either absent or the failing row's full
	# column values rather than a Key(...)= shape, so there's nothing
	# reliable to extract from message_detail. It still gets a more
	# specific message than the generic fallback, but via
	# constraint_name instead — see _classify_pg_by_sqlstate.
	_PG_EXTRACTABLE_SQLSTATES = frozenset({"23505", "23503", "23P01"})

	_PG_KEY_COLUMN_PATTERN = re.compile(r"key \((?P<columns>[^)]+)\)=")

	# SQLite extended result codes for SQLITE_CONSTRAINT.
	# https://sqlite.org/rescode.html#extrc
	# Verified directly against sqlite3 3.45 (Python 3.12): a UNIQUE
	# violation on a composite index still reports as
	# SQLITE_CONSTRAINT_UNIQUE, and a PRIMARY KEY violation reports as
	# SQLITE_CONSTRAINT_PRIMARYKEY even though its message text is
	# still "UNIQUE constraint failed: ..." (indistinguishable from a
	# plain UNIQUE violation by text alone).
	_SQLITE_ERRORNAME_MAP: dict[str, tuple[type[APIException.Base], str]] = {
		"SQLITE_CONSTRAINT_UNIQUE": (APIException.Conflict, "A unique value already exists"),
		"SQLITE_CONSTRAINT_PRIMARYKEY": (APIException.Conflict, "A record with this identifier already exists"),
		"SQLITE_CONSTRAINT_NOTNULL": (APIException.UnprocessableEntity, "A required field is missing"),
		"SQLITE_CONSTRAINT_CHECK": (APIException.UnprocessableEntity, "A validation rule was violated"),
		"SQLITE_CONSTRAINT_FOREIGNKEY": (APIException.Conflict, "A referenced record does not exist"),
		"SQLITE_CONSTRAINT_TRIGGER": (APIException.Conflict, "The operation was blocked by a database trigger"),
	}

	# Errornames for which SQLite's error text reliably contains a
	# parseable "table.column[, table.column, ...]" list, so a more
	# specific message can be built. CHECK is deliberately excluded:
	# verified that its text is either the raw boolean expression
	# ("age > 0") for unnamed constraints or the constraint's name
	# for named ones — neither is a column identifier, so extraction
	# would be wrong more often than it'd help.
	_SQLITE_EXTRACTABLE_ERRORNAMES = frozenset({
		"SQLITE_CONSTRAINT_UNIQUE",
		"SQLITE_CONSTRAINT_PRIMARYKEY",
		"SQLITE_CONSTRAINT_NOTNULL",
	})

	# Matches the "table.col, table.col2" (or bare "col, col2") tail
	# that SQLite appends after "... constraint failed: " for UNIQUE,
	# PRIMARY KEY, and NOT NULL violations.
	_SQLITE_COLUMN_LIST_PATTERN = re.compile(r"constraint failed:\s*(?P<columns>[\w.,\s]+)")

	# Ordered (pattern, exception, message_builder) triples used for
	# SQLite, and as a last-resort fallback for PostgreSQL errors with
	# no sqlstate at all (e.g. a driver that is neither psycopg nor
	# asyncpg).
	#
	# Each pattern captures the table/column identifiers SQLite embeds
	# in its error text, so the message_builder can produce a message
	# as specific as the Postgres column_name path gets — instead of a
	# constant generic string.
	_TEXT_DETECTORS: tuple[
		tuple[re.Pattern[str], type[APIException.Base], Callable[[re.Match[str]], str]],
		...,
	] = (
		(
			# "not null constraint failed: users.email"
			re.compile(r"not null constraint failed:\s*(?:(?P<table>\w+)\.)?(?P<column>\w+)"),
			APIException.UnprocessableEntity,
			lambda m: ErrorMessage.field_required(m.group("column")),
		),
		(
			# "unique constraint failed: users.email"
			re.compile(r"unique constraint failed:\s*(?:(?P<table>\w+)\.)?(?P<column>\w+)"),
			APIException.Conflict,
			lambda m: ErrorMessage.unique_constraint_violation(m.group("column")),
		),
		(
			# older SQLite phrasing: "column email is not unique"
			re.compile(r"column (?P<column>\w+) is not unique"),
			APIException.Conflict,
			lambda m: ErrorMessage.unique_constraint_violation(m.group("column")),
		),
		(
			# SQLite gives no table/column detail for FK violations.
			re.compile(r"foreign key constraint failed"),
			APIException.Conflict,
			lambda m: ErrorMessage.referential_integrity(),
		),
		(
			# "check constraint failed: users"
			re.compile(r"check constraint failed:\s*(?P<table>\w+)"),
			APIException.UnprocessableEntity,
			lambda m: f"A validation rule was violated on {m.group('table')}",
		),
	)

	@dataclass(frozen=True, slots=True)
	class _PgDiagnostics:
		"""
		Normalized view over PostgreSQL error diagnostics, regardless
		of which driver produced them.

		psycopg (sync) nests this information under `orig.diag`
		(a psycopg diagnostics object). asyncpg's own exceptions
		carry `sqlstate`, `constraint_name`, `column_name`,
		`table_name`, and `detail` as flat attributes — but
		SQLAlchemy's asyncpg dialect hands back a thin wrapper as
		`orig`, not that real exception, so it has to be unwrapped
		(via `orig.driver_exception` or `orig.__cause__`) before
		those flat attributes are actually populated. See
		`_get_pg_diagnostics` for where_fields that unwrapping happens.

		Building this once up front means the rest of the resolver
		(SQLSTATE classification, column extraction, constraint-name
		matching) never needs to know which driver produced the
		error, or that asyncpg needed unwrapping in the first place.
		"""

		sqlstate: str | None
		constraint_name: str | None
		column_name: str | None
		table_name: str | None
		message_detail: str | None

	@classmethod
	def _get_pg_diagnostics(cls, error: Exception) -> DatabaseErrorResolver._PgDiagnostics | None:
		"""
		Safely extract normalized PostgreSQL diagnostics from either
		supported driver.

		Returns:
			A `_PgDiagnostics` instance when `error.orig` looks like a
			PostgreSQL driver exception from either psycopg or
			asyncpg.
			None for SQLite or any driver this resolver doesn't
			recognize.

		Detection order:

		1. psycopg: `orig.diag` exists (a diagnostics object) ->
		   pull sqlstate/constraint_name/column_name/table_name/
		   message_detail off of `diag`.
		2. asyncpg: SQLAlchemy's asyncpg dialect does NOT hand back
		   the real `asyncpg.exceptions.PostgresError` as `orig`. It
		   wraps it in its own `AsyncAdapt_asyncpg_dbapi.Error`, and
		   that wrapper only forwards `pgcode`/`sqlstate` — NOT
		   `constraint_name`, `column_name`, `table_name`, or
		   `detail` (confirmed against SQLAlchemy issue #9843: on
		   that wrapper, `vars(orig)` is just
		   `{'pgcode': ..., 'sqlstate': ...}`, nothing else). So
		   reading those fields off `orig` directly always yields
		   None; the real asyncpg exception must be found first:
		     a. SQLAlchemy 2.1+: exposed as `orig.driver_exception`
		        (the new `EmulatedDBAPIException.driver_exception`
		        attribute documented for emulated-DBAPI dialects like
		        asyncpg).
		     b. Older SQLAlchemy: not exposed as a named attribute at
		        all, but still reachable via Python's own exception
		        chaining as `orig.__cause__`, since SQLAlchemy's
		        asyncpg adapter raises its wrapper with
		        `raise translated_error from error` — the documented
		        workaround from that same issue.
		   Once the real asyncpg exception is found, its `sqlstate`,
		   `constraint_name`, `column_name`, `table_name`, and
		   `detail` attributes are read directly (asyncpg has no
		   nested `diag` wrapper of its own).
		"""
		orig = getattr(error, "orig", None)
		if orig is None:
			return None

		# --- psycopg (sync): nested diagnostics object -------------
		diag = getattr(orig, "diag", None)
		if diag is not None:
			return cls._PgDiagnostics(
				sqlstate=getattr(diag, "sqlstate", None) or getattr(orig, "pgcode", None),
				constraint_name=getattr(diag, "constraint_name", None),
				column_name=getattr(diag, "column_name", None),
				table_name=getattr(diag, "table_name", None),
				message_detail=getattr(diag, "message_detail", None),
			)

		# --- asyncpg (async): unwrap SQLAlchemy's thin adapter error
		# to reach the real asyncpg.exceptions.PostgresError, which is
		# where_fields constraint_name/column_name/table_name/detail
		# actually live. `orig` itself only ever has pgcode/sqlstate.
		asyncpg_error = getattr(orig, "driver_exception", None) or getattr(orig, "__cause__", None)

		# Only trust this as "the real asyncpg exception" if it
		# actually carries a sqlstate — guards against `__cause__`
		# being something unrelated (e.g. None, or a chained error
		# from a completely different failure) on some SQLAlchemy /
		# driver versions.
		if asyncpg_error is not None and getattr(asyncpg_error, "sqlstate", None):
			return cls._PgDiagnostics(
				sqlstate=getattr(asyncpg_error, "sqlstate", None),
				constraint_name=getattr(asyncpg_error, "constraint_name", None),
				column_name=getattr(asyncpg_error, "column_name", None),
				table_name=getattr(asyncpg_error, "table_name", None),
				message_detail=getattr(asyncpg_error, "detail", None),
			)

		# Fallback: `orig` itself carries a bare `sqlstate` (covers
		# both the case where_fields SQLAlchemy's wrapper is all we have and
		# no richer exception could be found, and any driver that
		# puts sqlstate directly on `orig` without the asyncpg-style
		# wrapping). This still enables correct classification and
		# generic messaging even without constraint/column detail.
		sqlstate = getattr(orig, "sqlstate", None) or getattr(orig, "pgcode", None)
		if sqlstate is not None:
			return cls._PgDiagnostics(
				sqlstate=sqlstate,
				constraint_name=getattr(orig, "constraint_name", None),
				column_name=getattr(orig, "column_name", None),
				table_name=getattr(orig, "table_name", None),
				message_detail=getattr(orig, "detail", None),
			)

		return None

	@staticmethod
	def _get_sqlite_errorname(error: Exception) -> str | None:
		"""
		Safely extract the SQLite extended result code name, e.g.
		"SQLITE_CONSTRAINT_UNIQUE", "SQLITE_CONSTRAINT_FOREIGNKEY".

		This is the SQLite equivalent of Postgres's SQLSTATE: a stable,
		documented classification that doesn't depend on parsing
		human-readable error text. It requires Python 3.11+ (the
		`sqlite_errorcode` / `sqlite_errorname` attributes were added
		to the stdlib `sqlite3` module in that release) and is only
		set on errors that originated from the SQLite library itself.
		On older Python versions, or drivers where_fields this isn't
		populated, this returns None and classification falls back to
		text pattern matching.
		"""
		orig = getattr(error, "orig", None)
		return getattr(orig, "sqlite_errorname", None)


	@staticmethod
	def _match_constraint(
		constraints: list[DatabaseConstraint],
		*,
		constraint_name: str | None = None,
		db_error: str | None = None,
		debug_detail: str | None = None,
	) -> APIException.Base | None:
		"""
		Attempt to resolve a database error using explicitly configured
		DatabaseConstraint overrides.

		Matching order:

		1. PostgreSQL exact constraint-name match.
		2. SQLite identifier substring match.

		Returns:
			A configured API exception if a match is found.
			None otherwise (falls through to auto-detection).
		"""

		for constraint in constraints:

			if (
				constraint_name
				and constraint.constraint_name == constraint_name
			):
				return constraint.exception(
					constraint.message,
					debug_detail=debug_detail,
				)

			if (
				db_error
				and constraint.sqlite_identifier.lower() in db_error
			):
				return constraint.exception(
					constraint.message,
					debug_detail=debug_detail or db_error,
				)

		return None

	@classmethod
	def _extract_pg_key_columns(cls, message_detail: str | None) -> list[str]:
		"""
		Pull the column name(s) out of Postgres's standard constraint
		error detail, e.g. "Key (email)=(a@x.com) already exists." ->
		["email"], a composite key's "Key (user_id, org_id)=(1, 2)
		already exists." -> ["user_id", "org_id"], or an exclusion
		violation's "Key (room_id, during)=(1, [...)) conflicts with
		existing key (room_id, during)=(1, [...))." -> ["room_id",
		"during"] (only the first "Key (...)=" occurrence is parsed;
		exclusion violations repeat the same column list a second time
		for the conflicting row, so there's nothing extra to gain from
		matching further).

		This format is used for unique_violation, foreign_key_violation,
		and exclusion_violation details (confirmed against Postgres's
		own documentation examples), and is identical whether the
		detail text arrived via psycopg's `diag.message_detail` or
		asyncpg's `exception.detail` — both simply relay the server's
		DETAIL field verbatim. Returns [] if message_detail is absent
		or doesn't match — which can happen if the server's
		`lc_messages` locale isn't English, since DETAIL text is
		translated but SQLSTATE codes are not; callers must tolerate
		an empty result and fall back to the generic message.
		"""
		if not message_detail:
			return []

		match = cls._PG_KEY_COLUMN_PATTERN.search(message_detail.lower())
		if not match:
			return []

		return [
			column.strip()
			for column in match.group("columns").split(",")
			if column.strip()
		]

	@classmethod
	def _classify_pg_by_sqlstate(
		cls,
		diagnostics: DatabaseErrorResolver._PgDiagnostics,
	) -> APIException.Base | None:
		"""
		Build an APIException.Base from a Postgres SQLSTATE code, using
		column names extracted from `column_name` (not-null) or
		`message_detail` (unique / foreign-key / exclusion) for a
		specific message where_fields the format reliably provides them,
		`constraint_name` (check) where_fields no column can be reliably
		extracted, and falling back to the generic per-SQLSTATE
		message otherwise (e.g. when message_detail isn't in the
		expected shape, or no constraint_name is present).

		`diagnostics` is the normalized `_PgDiagnostics` produced by
		`_get_pg_diagnostics`, so this method itself doesn't need to
		know or care whether the underlying driver was psycopg or
		asyncpg.
		"""
		sqlstate = diagnostics.sqlstate
		if sqlstate is None or sqlstate not in cls._PG_SQLSTATE_MAP:
			return None

		exception_cls, generic_message = cls._PG_SQLSTATE_MAP[sqlstate]
		debug_detail = (
			f"pgcode={sqlstate} constraint={diagnostics.constraint_name} "
			f"table={diagnostics.table_name}"
		)

		if sqlstate == "23502" and diagnostics.column_name:
			return exception_cls(
				ErrorMessage.field_required(diagnostics.column_name),
				debug_detail=debug_detail,
			)

		# check_violation: message_detail doesn't reliably contain a
		# parseable column list (see _PG_EXTRACTABLE_SQLSTATES comment
		# above), but constraint_name is always populated by Postgres
		# for a named CHECK constraint, so use that for specificity
		# instead of the flat generic message.
		if sqlstate == "23514" and diagnostics.constraint_name:
			return exception_cls(
				f"The value violates the '{diagnostics.constraint_name}' rule",
				debug_detail=debug_detail,
			)

		if sqlstate in cls._PG_EXTRACTABLE_SQLSTATES:
			columns = cls._extract_pg_key_columns(diagnostics.message_detail)
			if columns:
				field = " and ".join(columns)
				if sqlstate == "23505":
					return exception_cls(
						ErrorMessage.unique_constraint_violation(field),
						debug_detail=debug_detail,
					)
				if sqlstate == "23503":
					return exception_cls(
						ErrorMessage.referential_integrity(field),
						debug_detail=debug_detail,
					)
				if sqlstate == "23P01":
					# Exclusion violations share the unique
					# violation's "already conflicts" shape
					# semantically (no two rows may coexist for this
					# column set), so a similarly-worded but distinct
					# message keeps it from being confused with a
					# plain unique violation in logs/responses.
					return exception_cls(
						f"A conflicting record already exists for {field}",
						debug_detail=debug_detail,
					)

		return exception_cls(generic_message, debug_detail=debug_detail)

	@classmethod
	def _extract_sqlite_columns(cls, db_error: str) -> list[str]:
		"""
		Pull the column name(s) out of a UNIQUE / PRIMARY KEY / NOT
		NULL error message, e.g. "unique constraint failed:
		users.email" -> ["email"], or a composite index's "unique
		constraint failed: memberships.user_id, memberships.org_id"
		-> ["user_id", "org_id"]. Returns [] if the text doesn't match
		the expected shape (message formats aren't 100% guaranteed
		across SQLite versions, so callers must tolerate an empty
		result and fall back to a generic message).
		"""
		match = cls._SQLITE_COLUMN_LIST_PATTERN.search(db_error)
		if not match:
			return []

		columns: list[str] = []
		for part in match.group("columns").split(","):
			# Each part may be "table.column" or a bare "column".
			identifier = part.strip().rsplit(".", 1)[-1]
			if re.fullmatch(r"\w+", identifier):
				columns.append(identifier)
		return columns

	@classmethod
	def _classify_sqlite_by_errorname(
		cls,
		db_error: str,
		errorname: str,
	) -> APIException.Base | None:
		"""
		Build an APIException.Base from a SQLITE_CONSTRAINT_* errorname,
		using extracted column names for a specific message where_fields the
		error text reliably provides them (UNIQUE / PRIMARY KEY / NOT
		NULL), and falling back to the generic per-errorname message
		otherwise (always the case for FOREIGN KEY and CHECK).
		"""
		if errorname not in cls._SQLITE_ERRORNAME_MAP:
			return None

		exception_cls, generic_message = cls._SQLITE_ERRORNAME_MAP[errorname]
		debug_detail = f"{errorname}: {db_error}"

		if errorname in cls._SQLITE_EXTRACTABLE_ERRORNAMES:
			columns = cls._extract_sqlite_columns(db_error)
			if columns:
				if errorname == "SQLITE_CONSTRAINT_NOTNULL":
					return exception_cls(
						ErrorMessage.field_required(columns[0]),
						debug_detail=debug_detail,
					)
				field = " and ".join(columns)
				return exception_cls(
					ErrorMessage.unique_constraint_violation(field),
					debug_detail=debug_detail,
				)

		return exception_cls(generic_message, debug_detail=debug_detail)

	@classmethod
	def _auto_detect_text(cls, db_error: str) -> APIException.Base | None:
		"""
		Classify a constraint violation by scanning the raw error text
		for known patterns, extracting table/column identifiers where_fields
		SQLite provides them so the message can be as specific as the
		Postgres column_name path. This is a fallback path only, used
		when `sqlite_errorname` isn't available (Python < 3.11, or a
		driver that doesn't populate it) — prefer
		`_classify_sqlite_by_errorname` when possible.
		"""
		for pattern, exception_cls, message_builder in cls._TEXT_DETECTORS:
			match = pattern.search(db_error)
			if match:
				return exception_cls(
					message_builder(match),
					debug_detail=db_error,
				)
		return None

	@classmethod
	def _fallback_debug_detail(cls, db_error: str) -> str:
		"""
		Build a consistent debug message for constraint violations that
		neither an explicit mapping nor auto-detection could classify.

		The returned message is intended for logs and debugging only.
		Client-facing responses remain generic and safe.
		"""
		return (
			f"{cls.FALLBACK_CONSTRAINT_MESSAGE}"
			f"Original error: {db_error}"
		)
	
	@classmethod
	def resolve(
		cls,
		*,
		error: Exception,
		constraints: Iterable[DatabaseConstraint] = (),
	) -> APIException.Base:
		"""
		Convert a database exception into an application-level
		HTTP exception.

		Resolution order: explicit constraint mapping -> automatic
		classification (SQLSTATE for Postgres — via either psycopg or
		asyncpg — for SQLite errorname/text matching) -> generic
		fallback.
		"""

		db_error = str(getattr(error, "orig", error)).lower()
		constraints = list(constraints)

		if isinstance(error, IntegrityError):

			diagnostics = cls._get_pg_diagnostics(error)

			# --- PostgreSQL path (psycopg or asyncpg) -----------------
			if diagnostics is not None:

				# 1. Explicit override by constraint name.
				if diagnostics.constraint_name:
					matched = cls._match_constraint(
						constraints,
						constraint_name=diagnostics.constraint_name,
						debug_detail=(
							f"pgcode={diagnostics.sqlstate} "
							f"constraint={diagnostics.constraint_name} "
							f"table={diagnostics.table_name}"
						),
					)
					if matched:
						return matched

				# 2. Automatic classification via SQLSTATE, with
				#    column names pulled from diagnostics where_fields the
				#    format supports it. This alone covers unique /
				#    FK / not-null / check / exclusion violations
				#    without needing constraints configured at all,
				#    on both driver families.
				if diagnostics.sqlstate:
					classified = cls._classify_pg_by_sqlstate(diagnostics)
					if classified:
						return classified

				# 3. Unrecognized SQLSTATE (rare) — generic fallback,
				#    still flagged for follow-up.
				return APIException.Conflict(
					"A database constraint was violated",
					debug_detail=cls._fallback_debug_detail(
						f"pgcode={diagnostics.sqlstate} "
						f"constraint={diagnostics.constraint_name} "
						f"table={diagnostics.table_name}"
					),
				)

			# --- SQLite (or any driver without PG diagnostics) path ---

			errorname = cls._get_sqlite_errorname(error)

			sqlite_debug_detail = (
				f"{errorname}: {db_error}"
				if errorname
				else db_error
			)

			# 1. Explicit override by table.column substring.
			matched = cls._match_constraint(
				constraints,
				db_error=db_error,
				debug_detail=sqlite_debug_detail,
			)
			if matched:
				return matched

			# 2. Automatic classification via SQLITE_CONSTRAINT_*
			#    errorname (Python 3.11+). This alone covers unique /
			#    FK / not-null / check / primary-key violations
			#    without needing constraints configured at all, and
			#    is more reliable than text matching since it doesn't
			#    depend on SQLite's error-message wording.
			if errorname:
				classified = cls._classify_sqlite_by_errorname(
					db_error,
					errorname,
				)
				if classified:
					return classified

			# 3. errorname unavailable (Python < 3.11, or a driver
			#    that doesn't expose it) — fall back to text matching.
			auto = cls._auto_detect_text(db_error)
			if auto:
				return auto

			# 4. Nothing matched — generic fallback.
			return APIException.Conflict(
				"A database constraint was violated",
				debug_detail=cls._fallback_debug_detail(db_error),
			)

		# The handlers below are not constraint-resolution paths.
		#
		# They represent infrastructure-level database failures where_fields
		# constraint classification is not applicable.
		#
		# Examples:
		# - Lost database connection
		# - Query execution failures
		# - Driver-level failures
		# - Unexpected DBAPI exceptions
		#
		# The original error is preserved only for debugging purposes.

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