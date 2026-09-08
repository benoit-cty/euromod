# 02: Prefactor: one heading-driven document builder

**What to build:** The Country Report path's logic that turns a headed text into legal units (preamble unit, one unit per heading, nested by heading level, ltree paths slugified and de-duplicated) is lifted into a shared builder in the ingester's core that takes a title, the text, a heading pattern and the reviewer-facing identity fields, and returns the parsed-document IR. The Country Report path calls it and behaves exactly as before. Nothing user-visible changes; this makes ticket 03 a thin caller.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] A core builder produces the same units, paths, unit types and version keys the Country Report parser produced, driven by a heading pattern rather than Markdown specifically
- [x] The Country Report parser is a thin caller of the builder; its existing tests pass unchanged
- [x] Heading detection is pluggable: Markdown `#` headings and HTML `h1`–`h6` (already stripped to text) are both expressible as patterns, with a test for each
- [x] A text with no detected headings yields a single unit holding the whole text, with a test

## Comments

**2026-09-08 — implemented.** `core/documents.py::build_document`, driven by `HEADING_PATTERNS` (markdown / html / numbered). The Country Report parser is a thin caller and its tests pass unchanged.
