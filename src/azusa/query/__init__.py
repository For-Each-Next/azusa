"""Query database of Wikimedia projects."""

from __future__ import annotations

__all__ = ("Database", "statements", "tables")

from azusa.query import statements, tables
from azusa.query._database import Database
