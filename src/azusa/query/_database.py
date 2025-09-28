"""Core database functionality for MediaWiki connections."""

from __future__ import annotations

__all__ = ("Database",)

from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    NamedTuple,
    Self,
    TypedDict,
)
from urllib.parse import urlencode

import polars as pl
from polars import DataType
from sqlalchemy import Engine, Row, Select, create_engine, text

if TYPE_CHECKING:
    from collections.abc import Mapping

    from polars.datatypes import DataTypeClass
    from sqlalchemy.engine.interfaces import DBAPIType

    from azusa.query._typing import PywikibotSite, Statement, StrMode


class ColumnInfo(NamedTuple):
    """Container for database column metadata.

    Attributes:
        name: The name of the database column.
        type_code: The type code of the database API.
    """

    name: str
    type_code: DBAPIType


class RawQueryResult(TypedDict):
    """Type definition for raw database query results.

    Attributes:
        column_info: Tuple of ColumnInfo objects describing each
            column's metadata.
        rows: Tuple of SQLAlchemy Row objects (tuples) containing
            the query result data.
    """

    column_info: tuple[ColumnInfo, ...]
    rows: tuple[Row[Any], ...]


def map_type_code(
    code: DBAPIType | int,
    str_mode: StrMode = "guess",
) -> pl.datatypes.DataTypeClass:
    """Map a database API type code to a Polars data type.

    For example, code 3 is mapped to `polars.datatypes.Int64`.

    Args:
        code: The database API type code to map.
        str_mode: How to handle string type codes. Can be 'str',
            'bytes', or 'guess'.

    Returns:
        The corresponding Polars data type.
    """
    mapping = MappingProxyType({
        1: pl.datatypes.Int64,
        2: pl.datatypes.Int64,
        3: pl.datatypes.Int64,
        4: pl.datatypes.Float64,
        5: pl.datatypes.Float64,
        6: pl.datatypes.Null,  # uncertain
        7: pl.datatypes.Datetime,
        8: pl.datatypes.Int64,
        10: pl.datatypes.Date,
        246: pl.datatypes.Decimal,
        247: "STR_TYPE",
        248: "STR_TYPE",
        249: "STR_TYPE",
        250: "STR_TYPE",
        252: "STR_TYPE",
        253: "STR_TYPE",
    })
    if (result := mapping.get(code, pl.datatypes.Unknown)) != "STR_TYPE":
        return result
    match str_mode:
        case "str":
            return pl.datatypes.String
        case "bytes":
            return pl.datatypes.Binary
    return pl.datatypes.Unknown


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
            column_info = tuple(
                ColumnInfo(name=x[0], type_code=x[1])
                for x in result.cursor.description
            )
            rows = tuple(result.fetchall())
        return RawQueryResult(column_info=column_info, rows=rows)

    def fetch(
        self,
        __stmt: Statement,
        /,
        str_mode: StrMode | None = None,
        schema_overrides: Mapping[str, DataTypeClass | DataType] | None = None,
    ) -> pl.DataFrame:
        """Execute a raw SQL statement and return a Polars DataFrame.

        This method executes a statement to retrieve raw data, maps the
        data types according to the given or inferred string mode, and
        returns the query result as a DataFrame.

        Args:
            __stmt: The SQL-like statement used to fetch data.
            str_mode: The string handling mode. Must be one of 'str',
                'bytes', or 'guess'. If not specified, 'str' for Select
                objects and 'bytes' for other cases.
            schema_overrides: Optional schema overrides for the
                resulting DataFrame.

        Returns:
            The collected Polars DataFrame containing the data.
        """
        str_mode_: StrMode
        if str_mode is None:
            str_mode_ = "str" if isinstance(__stmt, Select) else "bytes"
        else:
            str_mode_ = str_mode
        raw_data = self.fetch_raw(__stmt)
        schema = [
            (col.name, map_type_code(col.type_code, str_mode_))
            for col in raw_data["column_info"]
        ]
        lf = pl.LazyFrame(
            raw_data["rows"],
            schema,
            schema_overrides=schema_overrides,
            orient="row",
        )
        return lf.collect()

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
