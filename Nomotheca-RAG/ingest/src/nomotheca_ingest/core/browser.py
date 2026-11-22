"""The one headless-browser launcher (optional ``browser`` extra: Playwright).

Two paths need a real browser, each for one narrow thing: the Legifrance ELI
resolver reads the final URL of a redirect DataDome only lets a browser
follow (ADR 0002, Chromium), and a contributed PDF some portals serve only to
a browser is downloaded (sante.gouv.fr's Bulletin officiel, Firefox). Both
are optional: without the extra, or when anything goes wrong in the browser,
the caller gets None and falls back to its refusal.

    uv sync --extra browser && uv run playwright install chromium firefox
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

Engine = Literal["chromium", "firefox"]


def browser_available() -> bool:
    """True when Playwright (the ``browser`` extra) is installed."""
    try:
        import playwright.sync_api  # noqa: F401
    except Exception:
        return False
    return True


def with_browser[T](engine: Engine, action: Callable[[Any], T]) -> T | None:
    """Launch a headless ``engine``, run ``action(browser)``, always close it.

    None when Playwright is absent or anything in the browser fails: a page
    that wants a human is left to the human.
    """
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None
    try:
        with sync_playwright() as playwright:
            browser = getattr(playwright, engine).launch(headless=True)
            try:
                return action(browser)
            finally:
                browser.close()
    except Exception:
        return None
