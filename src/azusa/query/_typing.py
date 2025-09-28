"""Type hints."""

from __future__ import annotations

__all__ = (
    "PywikibotSite",
    "Statement",
    "StrMode",
)

from typing import Literal

import pywikibot
from sqlalchemy import Select, TextClause

# Pywikibot-related
type PywikibotSite = pywikibot.site.BaseSite


# SQLAlchemy-related
type Statement = Select | TextClause | str
type StrMode = Literal["str", "bytes"]
