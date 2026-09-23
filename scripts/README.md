# Scripts

- `md_to_pdf.py` — renders a Markdown report to PDF with full Hangul
  support (`Noto Sans CJK KR`). Usage: `python3 md_to_pdf.py in.md out.pdf`.
  Requires `pip install weasyprint markdown` and the `fonts-noto-cjk`
  system package (`apt-get install -y fonts-noto-cjk`) for Korean glyphs to
  render instead of tofu boxes. Used by the daily account-analysis Routine
  to turn each dated report in `accounts/*/reports/` into the PDF that gets
  sent to the user, per their standing preference that every file summary
  come back as a PDF with Korean notation checked.
