"""
Search a PDF for keyword occurrences and extract relevant pages.
Requires: pdfplumber (pip install pdfplumber)

Usage:
    python search_pdf.py REPORT.pdf KEYWORD [KEYWORD2 ...] [--pages 10-20] [--out OUTPUT.txt]

Examples:
    python search_pdf.py Y16_CR_SI.pdf sickness nadomestilo
    python search_pdf.py Y16_CR_SI.pdf "replacement rate" --pages 1-60
    python search_pdf.py Y16_CR_SI.pdf "Table 2.3" --out sick_pages.txt
"""
import sys
import argparse
import pdfplumber

sys.stdout.reconfigure(encoding='utf-8')


def search_pdf(pdf_path, keywords, page_range=None):
    """Return list of (page_num, preview) for pages matching any keyword."""
    hits = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        start, end = (page_range or (1, total))
        for pg in range(start, min(end + 1, total + 1)):
            text = pdf.pages[pg - 1].extract_text() or ''
            if any(kw.lower() in text.lower() for kw in keywords):
                preview = text[:200].replace('\n', ' ')
                hits.append((pg, preview))
    return hits


def extract_pages(pdf_path, page_nums):
    """Extract full text of specific pages."""
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for pg in page_nums:
            text = pdf.pages[pg - 1].extract_text() or ''
            results.append((pg, text))
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf', help='Path to PDF file')
    parser.add_argument('keywords', nargs='+', help='Keywords to search for')
    parser.add_argument('--pages', help='Page range to search, e.g. 1-60', default=None)
    parser.add_argument('--extract', help='Comma-separated page numbers to extract in full', default=None)
    parser.add_argument('--out', help='Output file path', default=None)
    args = parser.parse_args()

    page_range = None
    if args.pages:
        start, end = args.pages.split('-')
        page_range = (int(start), int(end))

    lines = []

    if args.extract:
        page_nums = [int(p.strip()) for p in args.extract.split(',')]
        pages = extract_pages(args.pdf, page_nums)
        for pg, text in pages:
            lines.append(f'=== PAGE {pg} ===\n{text}\n')
    else:
        hits = search_pdf(args.pdf, args.keywords, page_range)
        if hits:
            lines.append(f'Found keyword(s) on {len(hits)} page(s):')
            for pg, preview in hits:
                lines.append(f'  Page {pg}: {preview}')
        else:
            lines.append('No matches found.')

    output = '\n'.join(lines)

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Written to {args.out}')
    else:
        print(output)
