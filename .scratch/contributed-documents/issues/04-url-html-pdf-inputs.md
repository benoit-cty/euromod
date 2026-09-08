# 04: URL, HTML and PDF inputs

**What to build:** The `document` subcommand also accepts a URL, and both paths accept HTML and PDF. Given a URL, the ingester fetches it in Python, archives the raw response with its content type, and keys the instrument on the canonical URL (scheme and host lowercased, fragment dropped, trailing slash normalised), so the BOFiP page linked with two different anchors is one instrument. An HTML page is reduced to its main content block before unit building, with the raw page kept in the snapshot and in the unit text's HTML column. A PDF is extracted to plain text with a core dependency; a PDF with no detectable headings or numbered paragraphs becomes one unit. The ingester can also report a suggested title (page title, PDF metadata, file name) and a suggested validity date (a date found in the title or URL) for a given input, which the UI will prefill from later.

**Blocked by:** 03 (contribute a file from the CLI).

**Status:** done

- [x] URL input: fetched with a plain HTTP client, archived with origin URL, content type and sha256, identity is the canonical URL; tests pin the canonicalisation rules including fragment dropping
- [x] HTML: main-content extraction (`main` or `article`, else the largest text block) feeds the builder; navigation and footer text is absent from units; a test uses a page with nav, main and footer
- [x] PDF: a plain-text extractor is added as a core dependency; a small generated PDF with headings yields several units, one without yields a single unit; tests for both
- [x] Suggested title and suggested valid_from are computed from the input and exposed by the library function without loading anything; tests cover page title, PDF metadata, file name and a date in a title
- [x] Manual check: the BOFiP page and the Unedic circular PDF from the spec ingest from the CLI for FR, with kinds doctrine and circulaire, and their chunks are retrievable

## Comments

**2026-09-08 — implemented.** `core/extract.py` (HTML main block, pypdf, title/date suggestions). Verified on the real BOFiP page and a real-world PDF; the BOFiP page under two anchors stays one instrument.
