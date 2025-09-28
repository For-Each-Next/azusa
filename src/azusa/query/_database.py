"""Core database functionality for MediaWiki database connections."""

from __future__ import annotations

__all__ = ("Database",)

from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, Self, TypedDict
from urllib.parse import urlencode

from sqlalchemy import Engine, Row, create_engine, text

if TYPE_CHECKING:
    from sqlalchemy.engine.interfaces import DBAPIType

    from azusa.query._typing import PywikibotSite, Statement


class ColumnInfo(NamedTuple):
    """Container for database column metadata information.

    Attributes:
        name: The name of the database column.
        type_code: The type code of the database API.
    """

    name: str
    type_code: DBAPIType


class RawQueryResult(TypedDict):
    """Type definition for raw database query results.

    Attributes:
        schema: Tuple of ColumnInfo objects describing each column's
            metadata.
        data: Tuple of SQLAlchemy Row objects (tuples) containing the
            query result data.
    """

    schema: tuple[ColumnInfo, ...]
    data: tuple[Row[Any], ...]


class Database:
    """MediaWiki database connection manager."""

    __slots__ = ("_engine", "extension", "host", "project")

    _instances: ClassVar[dict[tuple[str, str | None], Database]] = {}

    def __new__(cls, project: str, extension: str | None = None) -> Self:
        """Create or return an existing instance.

        Args:
            project: MediaWiki project database name (e.g., 'zhwiki',
                'wikidatawiki').
            extension: Extension database name (e.g., 'termstore' for
                'wikidatawiki').

        Returns:
            Database instance for the specified configuration.
        """
        return cls._instances.setdefault(
            (project, extension),
            super().__new__(cls),
        )

    def __init__(self, project: str, extension: str | None = None) -> None:
        """Initialize database configuration.

        Args:
            project: MediaWiki project database name (e.g., 'zhwiki',
                'wikidatawiki').
            extension: Extension database name (e.g., 'termstore' for
                'wikidatawiki').
        """
        self.project = project
        self.extension = extension
        self.host = self._construct_host()
        self._engine = self._create_engine()

    def _construct_host(self) -> str:
        """Build database host identifier.

        Combines the project name with an optional extension to create
        the complete host string for database connections.

        Returns:
            Database host identifier.
        """
        if self.extension is None:
            return self.project
        return f"{self.extension}.{self.project}"

    def _create_engine(self) -> Engine:
        """Create a database engine.

        Returns:
            SQLAlchemy engine instance configured for this database.
        """
        uri_params = {
            "host": f"{self.host}.analytics.db.svc.wikimedia.cloud",
            "database": f"{self.project}_p",
            "charset": "utf8",
            "read_default_file": ".my.cnf",
        }
        uri = f"mysql+pymysql://?{urlencode(uri_params)}"
        return create_engine(uri)

    def fetch_raw(self, __stmt: Statement, /) -> RawQueryResult:
        """Execute a raw SQL statement and return raw data.

        Args:
            __stmt: The SQL statement to execute. Can be a string or an
                SQLAlchemy executable object.

        Returns:
            A dictionary containing column metadata and the result set.
            The column metadata is represented as a tuple of ColumnInfo
            objects, and the result set is a tuple of Row objects.
        """
        stmt = text(__stmt) if isinstance(__stmt, str) else __stmt
        with self._engine.connect() as connection, connection.begin():
            result = connection.execute(stmt)
            schema = tuple(
                ColumnInfo(name=x[0], type_code=x[1])
                for x in result.cursor.description
            )
            data = tuple(result.fetchall())
        return RawQueryResult(schema=schema, data=data)

    @classmethod
    def from_site(
        cls,
        site: PywikibotSite,
        extension: str | None = None,
    ) -> Self:
        """Create a Database instance from a Pywikibot Site object.

        Args:
            site: Pywikibot Site object (e.g., `Pywikibot.Site('zh')`).
            extension: Extension database name (e.g., 'termstore' for
                `Pywikibot.Site('wikidata')`).

        Returns:
            Database instance for the site.
        """
        project = site.dbName()
        return cls(project, extension)
