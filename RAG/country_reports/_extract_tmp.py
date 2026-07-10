import sys
mods = {}
for m in ("pypdf", "fitz", "pdfplumber", "pypdfium2"):
    try:
        __import__(m)
        mods[m] = True
    except ImportError:
        mods[m] = False
print(mods)

pdf = "/home/ben/Euromod/euromod/RAG/country_reports/Y16_CR_FR.pdf"
out = "/home/ben/Euromod/euromod/RAG/country_reports/_pages_8_27.txt"
first, last = 8, 27

if mods.get("fitz"):
    import fitz
    doc = fitz.open(pdf)
    with open(out, "w", encoding="utf-8") as f:
        for i in range(first - 1, last):
            f.write(f"\n===== PAGE {i+1} =====\n")
            f.write(doc[i].get_text())
    print("done fitz")
elif mods.get("pdfplumber"):
    import pdfplumber
    with pdfplumber.open(pdf) as doc, open(out, "w", encoding="utf-8") as f:
        for i in range(first - 1, last):
            f.write(f"\n===== PAGE {i+1} =====\n")
            f.write(doc.pages[i].extract_text() or "")
    print("done pdfplumber")
elif mods.get("pypdf"):
    from pypdf import PdfReader
    r = PdfReader(pdf)
    with open(out, "w", encoding="utf-8") as f:
        for i in range(first - 1, last):
            f.write(f"\n===== PAGE {i+1} =====\n")
            f.write(r.pages[i].extract_text() or "")
    print("done pypdf")
else:
    print("NO PDF LIB")
    sys.exit(1)
