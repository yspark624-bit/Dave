#!/usr/bin/env python3
"""Render a Korean markdown report to PDF.

Usage: python3 scripts/md_to_pdf.py reports/2026-09-18_roth-ira_daily.md [out.pdf]

Handles the subset of markdown the daily reports use: #/##/### headings,
pipe tables, - bullets, 1. numbered lists, --- rules, **bold**, `code`.
Korean text needs an embedded TTF; the script looks for Noto Sans KR in the
usual places and downloads it into ~/.cache/dave-fonts as a last resort.
"""
import os
import re
import sys
import urllib.request

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

CACHE = os.path.expanduser("~/.cache/dave-fonts")
GSTATIC = "https://fonts.gstatic.com/s/notosanskr/v36/"
FONT_SOURCES = {
    # weight -> (filename, list of candidate local paths)
    "regular": (
        "NotoSansKR-Regular.ttf",
        ["/usr/share/fonts/truetype/noto/NotoSansKR-Regular.ttf",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"],
    ),
    "bold": (
        "NotoSansKR-Bold.ttf",
        ["/usr/share/fonts/truetype/noto/NotoSansKR-Bold.ttf",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"],
    ),
}


def _find_font(weight):
    name, candidates = FONT_SOURCES[weight]
    search = [os.path.join(CACHE, name)] + candidates
    # session scratchpads sometimes already hold the downloaded copy
    scratch = os.environ.get("CLAUDE_SCRATCHPAD")
    if scratch:
        search.insert(0, os.path.join(scratch, name))
    for path in search:
        if os.path.exists(path):
            return path
    os.makedirs(CACHE, exist_ok=True)
    dest = os.path.join(CACHE, name)
    urllib.request.urlretrieve(GSTATIC + name, dest)
    return dest


def register_fonts():
    pdfmetrics.registerFont(TTFont("KR", _find_font("regular")))
    pdfmetrics.registerFont(TTFont("KR-Bold", _find_font("bold")))
    pdfmetrics.registerFontFamily("KR", normal="KR", bold="KR-Bold",
                                  italic="KR", boldItalic="KR-Bold")


INK = colors.HexColor("#1a1a1a")
MUTED = colors.HexColor("#5a5a5a")
RULE = colors.HexColor("#c8c8c8")
HEAD_BG = colors.HexColor("#eef1f5")


def styles():
    base = dict(fontName="KR", textColor=INK, alignment=TA_LEFT)
    return {
        "h1": ParagraphStyle("h1", fontName="KR-Bold", fontSize=17, leading=23,
                             spaceAfter=4, textColor=INK),
        "h2": ParagraphStyle("h2", fontName="KR-Bold", fontSize=13, leading=18,
                             spaceBefore=14, spaceAfter=6, textColor=INK),
        "h3": ParagraphStyle("h3", fontName="KR-Bold", fontSize=11, leading=16,
                             spaceBefore=10, spaceAfter=4, textColor=INK),
        "body": ParagraphStyle("body", fontSize=9.2, leading=14.6,
                               spaceAfter=5, **base),
        "muted": ParagraphStyle("muted", fontSize=8.4, leading=12.5,
                                spaceAfter=6, fontName="KR", textColor=MUTED),
        "bullet": ParagraphStyle("bullet", fontSize=9.2, leading=14.6,
                                 leftIndent=11, bulletIndent=2,
                                 spaceAfter=3, **base),
        "cell": ParagraphStyle("cell", fontSize=8.1, leading=11.4, **base),
        "cellhead": ParagraphStyle("cellhead", fontName="KR-Bold", fontSize=8.1,
                                   leading=11.4, textColor=INK),
    }


def inline(text):
    """markdown inline -> reportlab markup, escaping XML first."""
    text = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"~~(.+?)~~", r"<strike>\1</strike>", text)
    text = re.sub(r"`(.+?)`", r"<font color='#334155'>\1</font>", text)
    return text


def is_table_row(line):
    return line.startswith("|") and line.endswith("|")


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_table(rows, st, width):
    header, body = rows[0], rows[1:]
    ncols = len(header)
    data = [[Paragraph(inline(c), st["cellhead"]) for c in header]]
    for r in body:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(inline(c), st["cell"]) for c in r])
    # first column gets the slack; the rest share evenly
    rest = ncols - 1
    if rest:
        first = width * min(0.34, max(0.16, 1.9 / ncols))
        col_widths = [first] + [(width - first) / rest] * rest
    else:
        col_widths = [width]
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
        ("LINEBELOW", (0, 0), (-1, 0), 0.7, RULE),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def convert(md_path, pdf_path):
    register_fonts()
    st = styles()
    margin = 16 * mm
    width = A4[0] - 2 * margin
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            leftMargin=margin, rightMargin=margin,
                            topMargin=15 * mm, bottomMargin=15 * mm,
                            title=os.path.basename(md_path))
    flow = []
    lines = open(md_path, encoding="utf-8").read().split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if is_table_row(stripped):
            rows = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                cells = split_row(lines[i].strip())
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            flow.append(Spacer(1, 3))
            flow.append(build_table(rows, st, width))
            flow.append(Spacer(1, 7))
            continue
        if stripped.startswith("<!--"):
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.6, color=RULE))
            flow.append(Spacer(1, 6))
        elif stripped == "\\pagebreak":
            flow.append(PageBreak())
        elif stripped.startswith("### "):
            flow.append(Paragraph(inline(stripped[4:]), st["h3"]))
        elif stripped.startswith("## "):
            flow.append(Paragraph(inline(stripped[3:]), st["h2"]))
        elif stripped.startswith("# "):
            flow.append(Paragraph(inline(stripped[2:]), st["h1"]))
        elif stripped.startswith("> "):
            flow.append(Paragraph(inline(stripped[2:]), st["muted"]))
        elif re.match(r"^[-*] ", stripped) or re.match(r"^\d+\. ", stripped):
            indent = len(line) - len(line.lstrip())
            buf = [re.sub(r"^([-*]|\d+\.) ", "", stripped)]
            m = re.match(r"^(\d+)\.", stripped)
            bullet = f"{m.group(1)}." if m else "•"
            # fold continuation lines into the same paragraph
            while (i + 1 < len(lines) and lines[i + 1].strip()
                   and not re.match(r"^\s*([-*]|\d+\.) ", lines[i + 1])
                   and not is_table_row(lines[i + 1].strip())
                   and not lines[i + 1].lstrip().startswith("#")
                   and (len(lines[i + 1]) - len(lines[i + 1].lstrip())) > indent):
                i += 1
                buf.append(lines[i].strip())
            style = st["bullet"]
            if indent >= 2:
                style = ParagraphStyle("sub", parent=style,
                                       leftIndent=style.leftIndent + 12,
                                       bulletIndent=style.bulletIndent + 10)
            flow.append(Paragraph(inline(" ".join(buf)), style, bulletText=bullet))
        else:
            buf = [stripped]
            while (i + 1 < len(lines) and lines[i + 1].strip()
                   and not is_table_row(lines[i + 1].strip())
                   and not re.match(r"^\s*([-*#>]|\d+\.)\s", lines[i + 1])
                   and not re.fullmatch(r"-{3,}", lines[i + 1].strip())):
                i += 1
                buf.append(lines[i].strip())
            flow.append(Paragraph(inline(" ".join(buf)), st["body"]))
        i += 1

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("KR", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - margin, 9 * mm, str(canvas.getPageNumber()))
        canvas.restoreState()

    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    return pdf_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".pdf"
    print(convert(src, out))
