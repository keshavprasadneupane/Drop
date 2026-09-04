from typing import Any, Type, TypeVar, Generic, Optional, List, Set
from sqlalchemy import ClauseElement, ColumnElement, inspect, select, func, or_, and_
from sqlalchemy.sql import Select
from typing import Literal
from enum import Enum

M = TypeVar("M")  # Generic type variable bounded to SQLAlchemy DB Models
J = TypeVar("J")  # Generic type variable bounded to SQLAlchemy DB Models for join relations

class JoinType(Enum):
		"""
		Defines the types of SQL joins supported by the QueryBuilder.
		Supported values:
		"""
		INNER = "inner"
		OUTER = "outer"


class QueryBuilder(Generic[M]):
	"""A stateful, fluent interface builder to construct SQLAlchemy expressions via method chaining.

	Provides high-level abstractions for common database operations like exact-match /
	IN-list filtering, robust multi-column full-text searching, sorting, and dynamic raw
	expression injection, eliminating boilerplate setup across domain controllers.

	This builder is a data-layer utility and deliberately has no knowledge of the API
	layer — it raises plain Python exceptions (AttributeError, ValueError) rather than
	app-level HTTP exceptions. A bad field name here is always a caller bug (wrong
	string passed in code), never something an end user can act on, so it isn't an
	API-facing "error" — it's a 500 waiting to be caught by whatever boundary decorator
	wraps the call site (e.g. `handle_api_errors` / `handle_db_errors`).

	Note on `where_fields`: unlike SQLAlchemy's own `Query.filter_by` (which is equality-only),
	this builder's `where_fields` treats list/tuple/set values as an `IN` condition automatically.
	Worth knowing if you're used to vanilla SQLAlchemy conventions.

	Method Usage Highlights:
	```python
	# Basic filtering (equality, or IN-list when a value is a list/tuple/set)
	query = (
		QueryBuilder(Project)
		.where_fields(owner_id=user.id, is_archived=False, category_id=[1, 2, 3])
		.order_by("created_at")
		.get_stmt()
	)

	# Full-text search against a precomputed/generated tsvector column + GIN index
	# (use this once the table has real row counts — see `search()` docstring)
	query = (
		QueryBuilder(Project)
		.search(query_text="game engine", field_names=[], tsvector_column="search_vector")
		.get_stmt()
	)

	# Debugging mid-chain: str()/repr() renders the compiled SQL with literals inlined
	qb = QueryBuilder(Project).where_fields(status="active")
	print(qb)  # <QueryBuilder[Project]: SELECT ... WHERE project.status = 'active'>
	```

	Full Comprehensive Chain Example:
	```python
	query = (
		QueryBuilder(Project)
		.where_fields(status="active", category_id=selected_category)
		.search(query_text="modern kitchen renovation", field_names=["title", "description"])
		.where_expression(lambda m: m.budget >= min_budget if min_budget else None)
		.where_expression(distance_expr <= 25.0 if distance_expr is not None else None)
		.order_by(field_name_or_expr=distance_expr if distance_expr is not None else "created_at", descending=False)
		.get_stmt()
	)
	```
	"""
	



	class Meta:
		"""Meta class to hold configuration constants for QueryBuilder."""
		DEFAULT_LANGUAGE :str= "english"  # Default language for full-text search
		ALLOWED_JOIN_TYPES:set[JoinType] = {jointype for jointype in JoinType} 
		ALLOWED_JOIN_TYPES_STR:set[str] = ",".join([jointype.value for jointype in ALLOWED_JOIN_TYPES])

	def __init__(self, model: Type[M], base_query: Optional[Select] = None):
		"""Initializes the builder with a target model context.

		Args:
			model: The target SQLAlchemy model class (e.g., Project, User).
			base_query: An optional pre-existing Select statement. If omitted,
				a clean `select(model)` base is initiated.
		"""
		self.model = model
		self.query = base_query if base_query is not None else select(model)
		# Added to allow join tracking state
		self._joined_relations: Set[Type[Any]] = set()

	def where_fields(self, **kwargs: Any) -> "QueryBuilder[M]":
		"""Applies column filters using equality or membership matching.

		Scalar values produce an equality match (`column == value`).
		List, tuple, or set values automatically produce a membership
		match (`column.in_(value)`).

		A value of None is treated as "do not filter on this field"
		and is ignored entirely. If you need explicit NULL handling,
		use `not_null()` or `where_expression()`.

		Usage Example (simple — equality filter):
		```python
		query = (
			QueryBuilder(Project)
			.where_fields(status="active", owner_id=4)
			.get_stmt()
		)
		```

		Usage Example (complex — mixed equality + IN-list, with a None passthrough
		for an optional filter that wasn't supplied by the caller):
		```python
		query = (
			QueryBuilder(Project)
			.where_fields(
				status="active",
				category_id=[1, 2, 3],
				owner_id=selected_owner_id,  # None here just means "skip this filter"
			)
			.get_stmt()
		)
		```

		Args:
			**kwargs: Field names mapped to values.
				- Scalar value -> equality condition.
				- list / tuple / set -> IN condition.
				- None -> ignored.

		Raises:
			AttributeError: If a provided field does not exist on the model. This is
				always a caller bug (typo'd field name in code), not user input, so it
				should be left to bubble up to a generic error boundary.
		"""
		for field_name, value in kwargs.items():
			if value is None:
				continue
			try:
				column = getattr(self.model, field_name)
			except AttributeError as e:
				raise AttributeError(
					f"Model '{self.model.__name__}' has no valid field named '{field_name}'"
				) from e

			if isinstance(value, (list, tuple, set)):
				self.query = self.query.where(column.in_(value))
			else:
				self.query = self.query.where(column == value)

		return self

	def not_null(self, *field_names: str) -> "QueryBuilder[M]":
		"""Requires one or more fields to contain non-NULL values.

		This is useful when rows with missing values should be excluded
		from the result set.

		Usage Example (simple — single field):
		```python
		query = (
			QueryBuilder(Project)
			.not_null("owner_id")
			.get_stmt()
		)
		```

		Usage Example (complex — multiple required fields, chained with other filters):
		```python
		query = (
			QueryBuilder(Project)
			.not_null("owner_id", "latitude", "longitude")
			.where_fields(status="active")
			.get_stmt()
		)
		```

		Args:
			*field_names: One or more model field names that must not be NULL.

		Raises:
			AttributeError: If any field name does not exist on the model. Always a
				caller bug — the field list is code-defined, not user-supplied.
		"""
		for field_name in field_names:
			try:
				column = getattr(self.model, field_name)
			except AttributeError as e:
				raise AttributeError(
					f"Model '{self.model.__name__}' has no valid field named '{field_name}'"
				) from e

			self.query = self.query.where(column.isnot(None))

		return self

	def where_expression(self, expression: Any) -> "QueryBuilder[M]":
		"""
			Injects a raw SQLAlchemy clause or a dynamic, callable expression builder.

			By default, separate criteria are evaluated as logical AND conditions. To combine 
			clauses with an AND, you have two options:
			1. Call multiple consecutive `where_expression()` steps (best for clean, linear filters).
			2. Use the inline bitwise AND operator `&` within a single call (essential when nesting 
			an AND condition inside a larger bitwise OR block).

			To combine clauses with an OR, use a single `where_expression()` call with conditions 
			separated by the bitwise OR operator `|`.

			This is the most primitive and versatile filtering method in the architecture, allowing 
			arbitrary SQLAlchemy expressions to be applied directly to the query statement. It can serve 
			as the underlying foundational engine for all higher-level filtering derivatives.

			Use this method to evaluate complex, runtime-generated database expressions such as 
			compound OR logic, spatial distance calculations, text ranking formulas, inequalities, 
			ranges, subqueries, or EXISTS predicates.

			Callable detection: any object that is `callable()` and is NOT itself a
			SQLAlchemy `ClauseElement` is treated as a builder function and invoked with
			the model class. This correctly handles plain lambdas/functions as well as
			`functools.partial`, bound methods, or callable objects — not just the narrow
			case of a bare Python function.

			Args:
				expression: A raw SQLAlchemy binary expression, a SQL text clause, or a
					callable (lambda, function, partial, or callable object) that accepts
					the current model class and returns a valid SQLAlchemy expression (or None).

			Returns:
				Self: The QueryBuilder instance for fluent method chaining. No-ops safely
					if the expression or the callable's evaluation resolves to None.

			Usage Example (simple — raw expression):
			```python
			query = (
				QueryBuilder(Project)
				.where_expression(Project.views > 500)
				.get_stmt()
			)
			```

			Usage Example (complex — mixed bitwise & and | with role-based ternary checks):
			```python
			query = (
				QueryBuilder(Project)
				.where_expression(
					# Public viewers need the project to be ACTIVE (uses bitwise &)
					((Project.is_private == False) & (Project.status == "ACTIVE")) |
					
					# Owners and members bypass the status check
					((Project.owner_id == current_user_id) if current_user_id else False) |
					(Project.members.any(user_id=current_user_id) if current_user_id else False)
				)
				.get_stmt()
			)
			```

			Usage Example (complex — conditional lambda plus a functools.partial closure,
			either of which safely no-ops if their condition resolves to None):
			```python
			import functools

			query = (
				QueryBuilder(Project)
				.where_expression(
					lambda m: m.budget >= min_budget if min_budget is not None else None
				)
				.where_expression(
					functools.partial(lambda m, uid: m.owner_id == uid, uid=user.id)
				)
				.get_stmt()
			)
			```
		"""
		if expression is None:
			return self

		if callable(expression) and not isinstance(expression, ClauseElement):
			resolved = expression(self.model)
			if resolved is None:
				return self

			self.query = self.query.where(resolved)
		else:
			self.query = self.query.where(expression)

		return self

	def search(
		self,
		query_text: Optional[str],
		field_names: List[str],
		language: str = Meta.DEFAULT_LANGUAGE,
		tsvector_column: Optional[str] = None,
	) -> "QueryBuilder[M]":
		"""Applies a PostgreSQL full-text search across one or more columns.

		Two modes:

		1. Inline mode (default) — pass `field_names`. The specified columns are
		   concatenated into a single `tsvector` at query time, allowing PostgreSQL
		   to search across all requested fields in one shot. NULL values are
		   automatically converted to empty strings via COALESCE so a NULL field
		   doesn't prevent matches from other searchable fields. Simple to use, but
		   this computes the tsvector fresh on every query — fine for small/medium
		   tables, but it's a full-table-scan cost once row counts grow.

		2. Precomputed mode — pass `tsvector_column` (a generated/stored `tsvector`
		   column on the model, e.g. via a DB migration + GIN index). This skips the
		   inline concatenation entirely and searches directly against the indexed
		   column. Prefer this once a table is search-heavy or has real row volume;
		   `field_names` is ignored in this mode.

		Empty search strings are always ignored. If neither `field_names` nor
		`tsvector_column` is provided, this is a no-op.

		Usage Example (simple — inline concatenation across two columns):
		```python
		query = (
			QueryBuilder(Project)
			.search(query_text="cyberpunk game", field_names=["title", "summary"])
			.get_stmt()
		)
		```

		Usage Example (complex — precomputed tsvector column at scale, chained with
		a relevance-based sort):
		```python
		query = (
			QueryBuilder(Project)
			.search(query_text="cyberpunk game", field_names=[], tsvector_column="search_vector")
			.order_by(func.ts_rank(Project.search_vector, func.websearch_to_tsquery("english", "cyberpunk game")))
			.get_stmt()
		)
		```

		Args:
			query_text: Raw user search text.
			field_names: Model fields to concatenate into a search vector.
				Ignored when `tsvector_column` is provided.
			language: PostgreSQL text search configuration. Defaults to "english".
			tsvector_column: Optional name of a precomputed/generated tsvector column
				on the model. When provided, search runs directly against this column
				instead of building a tsvector inline on every call.

		Raises:
			AttributeError: If any requested field (or the tsvector column itself)
				does not exist on the model. Always a caller bug, not user input.
		"""
		if not query_text or (not field_names and not tsvector_column):
			return self

		try:
			ts_query = func.websearch_to_tsquery(language, query_text)

			if tsvector_column:
				ts_vector = getattr(self.model, tsvector_column)
			else:
				columns = [getattr(self.model, name) for name in field_names]

				# COALESCE each column so NULL values don't break concatenation
				safe_columns = [func.coalesce(col, "") for col in columns]

				# Insert spaces between columns so words don't run together
				concat_args = []
				for i, col_expr in enumerate(safe_columns):
					concat_args.append(col_expr)
					if i < len(safe_columns) - 1:
						concat_args.append(" ")

				ts_vector = func.to_tsvector(language, func.concat(*concat_args))

			# FIXED: Internal core fix from .where_fields() to .where()
			self.query = self.query.where(ts_vector.op("@@")(ts_query))

		except AttributeError as e:
			raise AttributeError(
				f"One of the requested search fields does not exist on model '{self.model.__name__}'."
			) from e

		return self




	def search_partial(
		self,
		case_sensitive: bool = False,
		mode: Literal["and", "or"] = "and",
		**field_queries: str,
	) -> "QueryBuilder[M]":
		"""Applies SQL LIKE/ILIKE substring filters to one or more model fields.

		Unlike PostgreSQL full-text search, this performs raw substring matching.
		This is useful for autocomplete-style behavior, partial word matching,
		usernames, identifiers, ticket numbers, and other scenarios where users
		expect partial text such as `"te"` to match `"Test"`.

		Each keyword argument represents a model field and its search value.
		Multiple field filters can be combined using either AND or OR semantics.

		AND mode (default):
			A row must satisfy every provided field filter.

		OR mode:
			A row may satisfy any of the provided field filters.

		Case sensitivity can be controlled via `case_sensitive`:
		- False (default): Uses ILIKE (case-insensitive).
		- True: Uses LIKE (case-sensitive).

		Fields whose value is None or an empty string are ignored.

		Usage Example (simple — single-field substring match):
		```python
		query = (
			QueryBuilder(Issue)
			.search_partial(title="bug")
			.get_stmt()
		)
		```

		Usage Example (complex — OR across two fields, case-sensitive):
		```python
		query = (
			QueryBuilder(Issue)
			.search_partial(
				title="Login",
				description="OAuth",
				mode="or",
				case_sensitive=True,
			)
			.get_stmt()
		)
		```

		Examples:
		```text
		Stored title: "Test"

		search_partial(title="t")   -> Match
		search_partial(title="te")  -> Match
		search_partial(title="tes") -> Match
		search_partial(title="est") -> Match

		Stored title: "Login Bug"
		Stored description: "OAuth callback failure"

		search_partial(
			title="login",
			description="oauth"
		)
		-> Match (AND mode)

		search_partial(
			title="login",
			description="missing"
		)
		-> No Match (AND mode)

		search_partial(
			title="login",
			description="missing",
			mode="or"
		)
		-> Match (OR mode)
		```

		Args:
			case_sensitive:
				When True uses SQL LIKE.
				When False uses SQL ILIKE.

			mode:
				How multiple field filters should be combined.

				- "and": Every field filter must match.
				- "or": At least one field filter must match.

			**field_queries:
				Keyword arguments where:
				- key = model field name
				- value = text to search for

				Example:
				```python
				search_partial(
					title="login",
					description="oauth"
				)
				```

		Returns:
			The current QueryBuilder instance for fluent chaining.

		Raises:
			AttributeError: If one of the requested fields does not exist on the
				model. Always a caller bug — the field names are code-defined.
		"""
		if not field_queries:
			return self

		try:
			conditions = []

			for field_name, query_text in field_queries.items():

				if query_text is None or query_text == "":
					continue

				column = getattr(self.model, field_name)

				pattern = f"%{query_text}%"

				condition = (
					column.like(pattern)
					if case_sensitive
					else column.ilike(pattern)
				)

				conditions.append(condition)

			if not conditions:
				return self

			self.query = self.query.where(
				and_(*conditions)
				if mode == "and"
				else or_(*conditions)
			)

		except AttributeError as e:
			raise AttributeError(
				f"One of the requested search fields does not exist on model '{self.model.__name__}'."
			) from e

		return self





	def order_by(
		self,
		field_name_or_expr: Any,
		descending: bool = True,
		*,
		skip_null: bool = False
	) -> "QueryBuilder[M]":
		"""Applies directional sorting using either a column name or a raw SQL expression.

		Safely returns self if the field name or sorting expression evaluates to None.

		Note: calling `order_by` more than once on the same builder STACKS sort keys rather
		than replacing them (this is standard SQLAlchemy `.order_by()` behavior) — e.g.
		`.order_by("created_at").order_by("name")` sorts by created_at, then by name as a
		tiebreaker. If you need the second call to override the first, build the final
		field/expression before calling `order_by` once.

		Pass skip_null=True to exclude rows where the sort target is NULL, rather than
		letting the DB scatter them to the front or back of the result set.

		Usage Example (simple — sort by column name):
		```python
		query = QueryBuilder(Project).order_by("created_at", descending=True).get_stmt()
		```

		Usage Example (complex — sort by a computed expression, excluding NULLs,
		with a conditional fallback to a plain column):
		```python
		query = (
			QueryBuilder(Project)
			.order_by(
				field_name_or_expr=distance_expr if distance_expr is not None else "created_at",
				descending=False,
				skip_null=distance_expr is not None,
			)
			.get_stmt()
		)
		```

		Args:
			field_name_or_expr: Can be a column string name (e.g., "created_at") OR a
				raw computed SQLAlchemy expression (e.g., distance_formula or func.ts_rank()).
			descending: Sorts highest-to-lowest if True, lowest-to-highest if False. Defaults to True.
			skip_null: If True, additionally requires the sort target to be NOT NULL in the DB.

		Raises:
			AttributeError: If the sorting string column name does not exist on the
				model. Always a caller bug — the field name is code-defined.
		"""
		if field_name_or_expr is None:
			return self

		# Raw computed SQL expression/formula (e.g. a distance calculation) — use it directly
		if not isinstance(field_name_or_expr, str):
			sort_target = field_name_or_expr
		else:
			# Standard string column name — resolve it against the model
			try:
				sort_target = getattr(self.model, field_name_or_expr)
			except AttributeError as e:
				raise AttributeError(
					f"Model '{self.model.__name__}' has no valid sorting field named '{field_name_or_expr}'"
				) from e

		if skip_null:
			# FIXED: Internal core fix from .where_fields() to .where()
			self.query = self.query.where(sort_target.isnot(None))

		self.query = self.query.order_by(sort_target.desc() if descending else sort_target.asc())
		return self

	def join_relation(
		self, 
		relation_model: Type[J], 
		join_type: JoinType = JoinType.INNER,
		on: Optional[ColumnElement[bool]] = None
	) -> "QueryBuilder[M]":
		"""Joins a related model to the current query context with an optional ON clause.

		If an explicit condition is passed to the `on` parameter, it will be used directly 
		to bind the join. If `on` is omitted, the builder will automatically inspect the 
		base model's relationship mappings to infer the foreign keys.

		Usage Example (simple — implicit relationship join):
		```python
		query = (
			QueryBuilder(Issue)
			.join_relation(Project)
			.where_expression(Project.is_open == False)
			.get_stmt()
		)
		```

		Usage Example (complex — explicit ON clause to disambiguate a model with
		multiple possible relationship paths, then filtered on the joined table):
		```python
		query = (
			QueryBuilder(Issue)
			.join_relation(User, join_type=JoinType.OUTER, on=(Issue.reporter_id == User.id))
			.where_expression(User.is_active == True)
			.get_stmt()
		)
		```

		Args:
			relation_model: The related SQLAlchemy model class to join (e.g., Project).
				Must be bound to the declarative base `Base`.
			join_type: Type of join operation. Accepts "inner" or "outer". Defaults to "inner".
			on: Optional explicit SQLAlchemy boolean binary expression to use as the ON clause.

		Returns:
			The QueryBuilder instance for fluid method chaining.

		Raises:
			ValueError: If an unsupported `join_type` is provided, or if `on` is
				omitted and the join target is ambiguous due to multiple matching
				relationship fields. Both are caller/config bugs, not user input.
			AttributeError: If the requested target model has no valid relationship
				to the base model.
		"""
		# Idempotency safety: skip execution if this relation table was already bound inside this builder context
		if relation_model in self._joined_relations:
			return self

		try:
			# 1. Validate join type string
			if join_type not in QueryBuilder.Meta.ALLOWED_JOIN_TYPES:
				raise ValueError(
					f"Invalid join_type '{join_type}'. Must be one of {QueryBuilder.Meta.ALLOWED_JOIN_TYPES_STR}."
				)

			# 2. If NO explicit ON clause is provided, run relationship inspection guardrails
			if on is None:
				relationships = [
					rel for rel in inspect(self.model).relationships 
					if rel.mapper.class_ == relation_model
				]

				if len(relationships) > 1:
					raise ValueError(
						f"Ambiguous join targeted toward '{relation_model.__name__}'. "
						f"Multiple foreign key targets found. Please provide an explicit 'on' expression."
					)

			# 3. Apply the join operation using the explicit or implicit ON condition
			if join_type == JoinType.INNER:
				self.query = self.query.join(relation_model, onclause=on)
			elif join_type == JoinType.OUTER:
				self.query = self.query.outerjoin(relation_model, onclause=on)
	
			# 4. Cache model registration to protect against duplicate joins
			self._joined_relations.add(relation_model)

		except (AttributeError, Exception) as e:
			if isinstance(e, ValueError):
				raise e

			raise AttributeError(
				f"Model '{self.model.__name__}' failed to join against '{relation_model.__name__}'."
			) from e

		return self

	def get_stmt(self) -> Select:
		"""Finalizes the builder chain and returns the raw executable SQLAlchemy Select object.

		Usage Example (simple — finalize a plain filtered query):
		```python
		statement = QueryBuilder(Project).where_fields(is_active=True).get_stmt()
		```

		Usage Example (complex — finalize a multi-clause chain before execution):
		```python
		statement = (
			QueryBuilder(Project)
			.where_fields(is_active=True)
			.search(query_text="rpg", field_names=["title", "description"])
			.order_by("created_at")
			.get_stmt()
		)
		result = await db.execute(statement)
		```
		"""
		return self.query

	def __repr__(self) -> str:
		"""Renders the currently-built query as compiled SQL for mid-chain debugging.

		Falls back to the raw `Select` repr if literal-bind compilation fails for a
		dialect-specific reason (e.g. some PostgreSQL-specific functions can't always
		compile with literal_binds outside an actual dialect context).

		Usage Example (simple — inspect a single filter):
		```python
		qb = QueryBuilder(Project).where_fields(status="active")
		print(qb)  # <QueryBuilder[Project]: SELECT ... WHERE project.status = 'active'>
		```

		Usage Example (complex — inspect mid-chain state before finalizing, e.g. while
		debugging why a search clause isn't matching):
		```python
		qb = (
			QueryBuilder(Project)
			.where_fields(status="active")
			.search(query_text="rpg", field_names=["title"])
		)
		print(qb)  # <QueryBuilder[Project]: SELECT ... WHERE project.status = 'active' AND ...>
		qb.order_by("created_at")  # chain continues unaffected by the print/debug step
		```
		"""
		try:
			compiled = self.query.compile(compile_kwargs={"literal_binds": True})
			return f"<QueryBuilder[{self.model.__name__}]: {compiled}>"
		except Exception:
			return f"<QueryBuilder[{self.model.__name__}]: {self.query!r}>"