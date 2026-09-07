#!/usr/bin/env python3
import sys
import markdown
from weasyprint import HTML, CSS

md_path, pdf_path = sys.argv[1], sys.argv[2]
with open(md_path, encoding="utf-8") as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=["tables"])

css = """
@page { size: A4; margin: 18mm 15mm; }
body { font-family: "Noto Sans CJK KR", "Noto Sans KR", sans-serif; font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; }
h1 { font-size: 16pt; border-bottom: 2px solid #333; padding-bottom: 6px; }
h2 { font-size: 13pt; margin-top: 22px; border-left: 4px solid #444; padding-left: 8px; }
h3 { font-size: 11.5pt; margin-top: 16px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 16px 0; font-size: 9pt; }
th, td { border: 1px solid #999; padding: 5px 6px; text-align: left; vertical-align: top; }
th { background: #eef1f5; font-weight: 700; }
tr:nth-child(even) td { background: #fafafa; }
code { font-family: monospace; background: #f0f0f0; padding: 1px 3px; }
strong { color: #111; }
hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
em { color: #555; }
"""

html_doc = f"<html><head><meta charset='utf-8'></head><body>{html_body}</body></html>"
HTML(string=html_doc).write_pdf(pdf_path, stylesheets=[CSS(string=css)])
print("wrote", pdf_path)
