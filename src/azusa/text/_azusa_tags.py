"""Utilities for working with named HTML-style comment sections.

This module allows for the creation, identification, and manipulation of
delimited comment blocks in text, such as:

    <!-- azusa start="section_id" -->...<!-- azusa end="section_id" -->

These tags are useful for updating embedded content within wikitext.
"""

from __future__ import annotations

__all__ = ("AzusaTags",)

import re
from typing import ClassVar, Literal, Self


class AzusaTags:
    r"""Represent a named tag pair for marking sections with comments.

    These tags are designed to be used as markers to wrap content
    sections that can be programmatically accessed or replaced without
    side effect against rendered page.

    Examples:
        >>> foo_tags = AzusaTags("foo")
        >>> foo_tags.start
        '<!-- azusa start="foo" -->'
        >>> foo_tags.end
        '<!-- azusa end="foo" -->'
        >>> t = '<!-- azusa start="foo" -->neko<!-- azusa end="foo" -->'
        >>> foo_tags.extract_content(t)
        'neko'
        >>> foo_tags.replace_content(t, "inu")
        '<!-- azusa start="foo" -->inu<!-- azusa end="foo" -->'
    """

    __slots__ = ("name",)

    _instances: ClassVar[dict[str, Self]] = {}

    _TAG_TEMPLATE = '<!-- azusa {pos}="{name}" -->'

    def __new__(cls, name: str) -> Self:
        """Create or return a cached instance for the given name.

        Args:
            name: The tag identifier (e.g., "foo").

        Returns:
            The corresponding tag instance (newed or cached).
        """
        return cls._instances.setdefault(name, super().__new__(cls))

    def __init__(self, name: str) -> None:
        """Initialize a new instance.

        Args:
            name: The name used in the start and end tags.
        """
        self.name = name

    def _tag(self, pos: Literal["start", "end"]) -> str:
        """Generate a comment tag string for the given position.

        Args:
            pos: The position of the tag. One of 'start' or 'end'.

        Returns:
            The full comment tag string.
        """
        return self._TAG_TEMPLATE.format(pos=pos, name=self.name)

    @property
    def start(self) -> str:
        """Get the opening comment tag for the current name.

        Returns:
            The start tag, e.g., '<!-- azusa start="foo" -->'.
        """
        return self._tag("start")

    @property
    def end(self) -> str:
        """Get the closing comment tag for the current name.

        Returns:
            The end tag, e.g., '<!-- azusa end="foo" -->'.
        """
        return self._tag("end")

    @property
    def section_pattern(self) -> re.Pattern:
        """Get a compiled regex pattern to match the entire section.

        The pattern captures everything between the start and end tags.

        Returns:
            A compiled regular expression for section extraction.
        """
        ptn_str = (
            rf"{re.escape(self.start)}"
            r"(.*?)"
            rf"{re.escape(self.end)}"
        )
        return re.compile(ptn_str, flags=re.DOTALL)

    def make_section(self, content: str = "") -> str:
        """Construct a section with two tags around the given content.

        Args:
            content: The content to wrap. Defaults to an empty string.

        Returns:
            The formatted section string.
        """
        return f"{self.start}{content}{self.end}"

    def extract_content(self, text: str) -> str | None:
        """Extract the inner content of the section from the text.

        If multiple sections with the same tag name exist, only the
        first one will be extracted. If the tags are not found, returns
        None.

        Args:
            text: The text from which to extract the content of the tag.

        Returns:
            The content inside the first section if found, otherwise
            None.
        """
        if matches := self.section_pattern.search(text):
            return matches.group(1)
        return None

    def replace_content(self, text: str, new: str, *, count: int = 0) -> str:
        """Replace the content inside the section with new content.

        If multiple sections are found, replaces the inner content of up
        to `count` occurrences. If `count` is zero (default), all
        occurrences are replaced.

        If no section is found, the original text is returned unchanged.

        Args:
            text: The text containing the section(s) to be modified.
            new: The new content to insert between the tags.
            count: The maximum number of replacements to perform.
                Defaults to 0, which means replace all occurrences.

        Returns:
            str: The updated text with the content replaced.
        """
        new_content = self.make_section(new)
        return self.section_pattern.sub(new_content, text, count=count)
