"""Utilities for working with named HTML comment sections.

Useful for updating specific parts of Wikitext using sections like:
``<!-- tag start name="id" -->content<!-- tag end name="id" -->``
"""

from __future__ import annotations

__all__ = (
    "end_tag",
    "get_section_content",
    "make_section",
    "start_tag",
    "update_section",
)

import re


def start_tag(name: str) -> str:
    """Return the start comment tag for a named section.

    Args:
        name: The section identifier.

    Returns:
        An opening HTML comment tag.

    Examples:
        >>> start_tag("report")
        '<!-- tag start name="report" -->'
    """
    return f'<!-- tag start name="{name}" -->'


def end_tag(name: str) -> str:
    """Return the end comment tag for a named section.

    Args:
        name: The section identifier.

    Returns:
        A closing HTML comment tag.

    Examples:
        >>> end_tag("report")
        '<!-- tag end name="report" -->'
    """
    return f'<!-- tag end name="{name}" -->'


def make_section(name: str, content: str = "") -> str:
    """Wrap content with a pair of named comment tags.

    Args:
        name: The section identifier.
        content: The content to enclose. Defaults to empty.

    Returns:
        A full HTML comment block with tags and content.

    Examples:
    >>> make_section("foo", "neko")
    '<!-- tag start name="foo" -->neko<!-- tag end name="foo" -->'
    """
    return f"{start_tag(name)}{content}{end_tag(name)}"


def get_section_content(name: str, text: str) -> str | None:
    """Get content between named comment tags.

    Args:
        name: The section identifier to extract.
        text: The full text to search in.

    Returns:
        The section content, or None if not found.

    Examples:
        >>> tag_name = "foo"
        >>> text = make_section(tag_name, "neko")
        >>> get_section_content(tag_name, text)
        'neko'
    """
    open_tag = re.escape(start_tag(name))
    close_tag = re.escape(end_tag(name))
    pattern = re.compile(rf"{open_tag}(.*?){close_tag}", re.DOTALL)
    if match := pattern.search(text):
        return match.group(1)
    return None


def update_section(name: str, text: str, content: str) -> str | None:
    """Replace a section's content with new content.

    Args:
        name: The section identifier to update.
        text: The full text containing the section.
        content: The new content to insert.

    Returns:
        The updated section, or None if section not found.

    Examples:
        >>> tag_name = "foo"
        >>> text = make_section(tag_name, "neko")
        >>> new_text = update_section(tag_name, text, "inu")
        >>> get_section_content(tag_name, new_text)
        'inu'
    """
    ptn = (
        rf"{re.escape(start_tag(name))}"
        r".*?"
        rf"{re.escape(end_tag(name))}"
    )
    new_section = make_section(name, content)
    return re.sub(ptn, new_section, text, flags=re.DOTALL)
