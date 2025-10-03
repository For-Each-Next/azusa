"""Type hints."""

from __future__ import annotations

__all__ = (
    "PywikibotSite",
    "Statement",
    "StrMode",
)

from typing import Literal

from pywikibot.site._basesite import BaseSite  # noqa: PLC2701
from sqlalchemy import Select, TextClause

# Pywikibot-related
type PywikibotSite = BaseSite


# SQLAlchemy-related
type Statement = Select | TextClause | str
type StrMode = Literal["str", "bytes", "guess"]
