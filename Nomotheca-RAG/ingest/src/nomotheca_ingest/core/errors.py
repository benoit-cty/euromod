"""Errors that mean something to the person who started the run."""

from __future__ import annotations


class RefusalError(ValueError):
    """A reviewer-facing refusal: the request is understood and declined.

    An incomplete declaration, an unknown kind, a URL that names a whole code
    or answers with a page instead of the PDF. The CLI reports these as the
    message they are (exit code 2); any other error — a parser's ValueError
    included — fails as an error, with its traceback.
    """
