"""
Extract paragraphs from an OOXML (.docx) file.
Handles split text runs (common in policy table cells).

Usage:
    python extract_docx.py FILENAME.docx [OUTPUT.txt]
"""
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

def extract_paragraphs(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        with z.open('word/document.xml') as doc:
            tree = ET.parse(doc)
    results = []
    for i, para in enumerate(tree.findall(f'.//{ns}p')):
        text = ''.join(r.text or '' for r in para.findall(f'.//{ns}t'))
        if text.strip():
            results.append((i, text.strip()))
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python extract_docx.py FILENAME.docx [OUTPUT.txt]')
        sys.exit(1)

    docx_path = sys.argv[1]
    paras = extract_paragraphs(docx_path)

    output = '\n'.join(f'[{i}] {text}' for i, text in paras)

    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Written {len(paras)} paragraphs to {sys.argv[2]}')
    else:
        print(output)
