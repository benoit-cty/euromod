# Fallback Ladder for Inaccessible Web Sources

When a source is inaccessible (JS-rendered, 404, or blocked), work through these steps **in order** before giving up. Use only official documents or sites that host official documents verbatim.

## Step 1 — Official circulars and decisions on legal databases

Many tax/social insurance agencies publish binding circulars and ministerial decisions as PDFs. These are often indexed by legal databases that serve plain HTML.

| Country | Legal database | What it covers |
|---|---|---|
| EL (Greece) | taxheaven.gr, e-nomothesia.gr | EFKA circulars, ministerial decisions (Υπουργικές Αποφάσεις) |
| SI (Slovenia) | pisrs.si (Official Gazette) | All laws and regulations; free PDF download |
| FR (France) | legifrance.gouv.fr | All decrees and ministerial orders; static HTML |
| DE (Germany) | gesetze-im-internet.de | Federal laws; static HTML |
| All EU | EUR-Lex (eur-lex.europa.eu) | EU directives, transpositions, social security regulations |
| All countries | web.archive.org | Cached snapshots of official pages (use `https://web.archive.org/web/YEAR*/[URL]`) |

⚠️ Only use non-official websites (taxheaven, pisrs, legifrance etc.) when they host the **full text of an official document verbatim** (circulars, gazette issues, ministerial decisions). Do not use news articles, commentaries, or summaries.

## Step 2 — Official Gazette PDFs

Most countries publish rate changes via their Official Gazette (ΦΕΚ in Greece, Uradni list in Slovenia, Journal officiel in France, Bundesgesetzblatt in Germany). Search for the gazette issue enacting the specific rate change (e.g. search `ΦΕΚ EFKA 2026 ημερομίσθιο`) and fetch the PDF directly.

## Step 3 — Printer-friendly / alternative URL variants

Try:
- Append `?print=1` or `?format=print`
- Replace `www.` with `m.` (mobile version)
- Try `/en/` instead of home page for English variants
- Try direct subpage URLs (e.g. `/rates/`, `/amounts/`, `/visina-nadomestila/`)

## Step 4 — Ask the user

Only after exhausting steps 1–3. State exactly what value or document is missing and why no official source was reachable.
