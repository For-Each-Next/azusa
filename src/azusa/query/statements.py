"""SQL query statement builders for MediaWiki Database.

This module contains reusable SQLAlchemy query builder functions that
generate select statements for querying MediaWiki databases.
"""

from __future__ import annotations

__all__ = ("query_pages_by_wikiproject",)

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from sqlalchemy import BinaryExpression, Select, select

from azusa.query.tables import (
    Page,
    PageAssessments as Pa,
    PageAssessmentsProjects as Pap,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from sqlalchemy import BinaryExpression, Select
    from sqlalchemy.orm import InstrumentedAttribute


def _generate_where_clause(
    column: InstrumentedAttribute,
    value: str | float | Iterable[str | float],
) -> BinaryExpression:
    """Filter a column based on the specified value or values.

    Args:
        column: The column to filter.
        value: The value or values of values to filter by.

    Returns:
        Union: A condition representing the filter condition.
    """
    if isinstance(value, str):
        return column.op("=")(value)
    try:
        return column.in_(set(value))
    except TypeError:
        return column.op("=")(value)


def where_clauses(
    conditions: Iterable[tuple[InstrumentedAttribute, Any]],
) -> list[BinaryExpression]:
    """Generate filter conditions from column-value pairs.

    This is a convenience function that applies `generate_column_filter`
    to multiple column-value pairs and filters out None results.

    Args:
        conditions: Variable number of tuples, each containing a column
            and its corresponding filter value. If the value is None, no
            filter is generated for that column.

    Returns:
        A tuple of filter expressions, excluding any None results.
    """
    return [
        _generate_where_clause(col, val)
        for col, val in conditions
        if val is not None
    ]


def query_pages_by_wikiproject(
    __name: str | Iterable[str] | None = None,
    /,
    quality: str | Iterable[str] | None = None,
    priority: str | Iterable[str] | None = None,
) -> Select[tuple[int, int, str, str, str | None, str | None]]:
    """Build a query to select pages and assessments by WikiProject(s).

    Constructs an SQLAlchemy query that joins the ``Page``,
    ``PageAssessments``, and ``PageAssessmentsProjects`` tables to
    retrieve pages associated with the specified WikiProject(s),
    optionally filtered by 'class' and 'importance' assessments.

    Use relevant local project titles and grade names. For example, on
    the Chinese Wikipedia, use '电子游戏' for WikiProject Video games
    and '乙' for B-Class.

    Args:
        __name: One or more WikiProject or taskforce names to query.
            If `None` is provided, all projects are included, not just
            the project-independent assessment (PIQA).
        quality: One or more 'class' assessments to filter by.
        priority: One or more 'importance' assessments to filter by.

    Returns:
        A select statement with the following fields selected —
            ``page_id`` (integer),
            ``page_namespace`` (integer),
            ``page_title`` (string),
            ``pap_project_title`` (string),
            ``pa_class`` (nullable string),
            ``pa_importance`` (nullable string).
    """
    fields = [
        Page.page_id,
        Page.page_namespace,
        Page.page_title,
        Pap.pap_project_title,
        Pa.pa_class,
        Pa.pa_importance,
    ]
    conditions = [
        (Pap.pap_project_title, __name),
        (Pa.pa_class, quality),
        (Pa.pa_importance, priority),
    ]
    return (
        select(*fields)
        .where(*where_clauses(conditions))
        .select_from(Pap)
        .join(Pa, Pap.pap_project_id == Pa.pa_project_id)
        .join(Page, Pa.pa_page_id == Page.page_id)
    )
