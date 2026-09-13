#!/usr/bin/env python3
"""스크리닝 결과를 PDF로 인쇄 가능한 한글 HTML 리포트로 변환.

외부 라이브러리 불필요. 브라우저에서 열고 Ctrl+P -> "PDF로 저장" 하면 끝.
(reportlab/weasyprint 설치 없이도 PDF를 얻는 가장 확실한 무료 경로)

사용법:
    python3 scripts/make_report.py                       # out/screen.csv -> out/report.html
    python3 scripts/make_report.py out/screen.csv out/report.html
"""
import csv
import datetime
import html
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = """
@page { size: A4 landscape; margin: 14mm; }
* { box-sizing: border-box; }
body { font-family: "Malgun Gothic","Apple SD Gothic Neo","Noto Sans KR",sans-serif;
       margin: 0; padding: 24px; color: #1a1a1a; background: #fff; font-size: 12px; }
h1 { font-size: 20px; margin: 0 0 4px; }
.sub { color: #666; font-size: 11px; margin-bottom: 18px; }
table { width: 100%; border-collapse: collapse; margin-bottom: 22px; }
th { background: #f1f3f5; text-align: left; padding: 7px 8px; font-size: 11px;
     border-bottom: 2px solid #ced4da; white-space: nowrap; }
td { padding: 6px 8px; border-bottom: 1px solid #e9ecef; white-space: nowrap; }
tr:nth-child(even) td { background: #fafbfc; }
.num { text-align: right; font-variant-numeric: tabular-nums; }
.s2 { color: #0b7a3b; font-weight: 700; }
.s3 { color: #b8860b; font-weight: 600; }
.s4 { color: #c0392b; font-weight: 600; }
.s1 { color: #6c757d; }
.pos { color: #0b7a3b; } .neg { color: #c0392b; }
.tag { background:#e7f5ec; color:#0b7a3b; padding:1px 6px; border-radius:9px; font-size:10px; }
.note { font-size: 10.5px; color: #555; line-height: 1.7; border-top: 1px solid #dee2e6; padding-top: 10px; }
h2 { font-size: 14px; margin: 18px 0 8px; }
@media print { body { padding: 0; } }
"""

STAGE_CLS = {"Stage 2": "s2", "Stage 3": "s3", "Stage 4": "s4", "Stage 1": "s1"}
COLS = [
    ("ticker", "종목"), ("stage", "국면"), ("passed", "트렌드템플릿"), ("rs_pct", "RS"),
    ("price", "주가"), ("ext50", "50일선 이격"), ("from_high", "52주고점 대비"),
    ("from_low", "52주저점 대비"), ("ma200_slope", "200일선 기울기"),
    ("ret_3m", "3개월 수익률"), ("vcp", "신호"), ("fit", "추천 계좌"),
]
PCT_COLS = {"ext50", "from_high", "from_low", "ma200_slope", "ret_3m"}


def cell(key, raw):
    if key == "stage":
        return '<td class="%s">%s</td>' % (STAGE_CLS.get(raw, ""), html.escape(raw))
    if key == "passed":
        return '<td class="num">%s / 8</td>' % html.escape(raw)
    if key == "vcp":
        return "<td>%s</td>" % ('<span class="tag">%s</span>' % html.escape(raw) if raw else "")
    if key in PCT_COLS:
        try:
            v = float(raw)
        except ValueError:
            return "<td></td>"
        return '<td class="num %s">%+.1f%%</td>' % ("pos" if v >= 0 else "neg", v)
    if key in ("price", "rs_pct"):
        try:
            v = float(raw)
        except ValueError:
            return "<td></td>"
        return '<td class="num">%s</td>' % ("%.2f" % v if key == "price" else "%d" % v)
    return "<td>%s</td>" % html.escape(raw)


def table(rows):
    out = ["<table><thead><tr>"]
    out += ["<th>%s</th>" % h for _, h in COLS]
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append("<tr>" + "".join(cell(k, r.get(k, "")) for k, _ in COLS) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def main(argv):
    src = argv[0] if argv else os.path.join(ROOT, "out", "screen.csv")
    dst = argv[1] if len(argv) > 1 else os.path.join(ROOT, "out", "report.html")
    if not os.path.exists(src):
        print("입력 파일 없음: %s\n먼저 실행: python3 scripts/stage2_screen.py --csv out/screen.csv" % src)
        return 1

    with open(src, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    rows = [r for r in rows if r.get("ticker") != "SPY"]
    s2 = [r for r in rows if r.get("stage") == "Stage 2"]
    rest = [r for r in rows if r.get("stage") != "Stage 2"]
    asof = rows[0].get("date", "") if rows else ""

    body = [
        "<h1>Stage 2 모멘텀 스크리닝 리포트</h1>",
        '<div class="sub">기준일 %s &nbsp;|&nbsp; 생성 %s &nbsp;|&nbsp; '
        'William O&#39;Neil CANSLIM + Mark Minervini 트렌드 템플릿</div>'
        % (html.escape(asof), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "<h2>1. Stage 2 종목 (매수 · 보유 대상) — %d개</h2>" % len(s2),
        table(s2) if s2 else "<p>조건을 만족하는 Stage 2 종목이 없습니다. 현금 비중을 유지하십시오.</p>",
        "<h2>2. 그 외 감시 종목 — %d개</h2>" % len(rest),
        table(rest) if rest else "<p>해당 없음</p>",
        '<div class="note">'
        "<b>국면 해석</b> — Stage 1 바닥 다지기(관찰) / <b>Stage 2 상승 추세(매수·보유)</b> / "
        "Stage 3 천정권(분할 익절) / Stage 4 하락 추세(회피·청산)<br>"
        "<b>트렌드 템플릿</b> — Minervini 8개 조건 통과 수. 7/8 이상만 매수 후보로 간주.<br>"
        "<b>RS</b> — 상대강도 백분위(1~99). O&#39;Neil 기준 80 이상 권장, 신고가 돌파주는 90 이상.<br>"
        "<b>50일선 이격</b> — +5% 이내일 때 위험 대비 수익비가 가장 유리. +10% 초과는 추격 매수 금지.<br>"
        "<b>추천 계좌</b> — Webull(단기 스윙) / Roth IRA(중기) / 401k(장기, Principal·Ascensus).<br>"
        "<b>면책</b> — 본 리포트는 기계적 계산 결과이며 투자 자문이 아닙니다. 최종 판단과 책임은 투자자 본인에게 있습니다."
        "</div>",
    ]

    doc = ("<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\">"
           "<title>Stage 2 모멘텀 스크리닝 리포트</title><style>%s</style></head><body>%s</body></html>"
           % (CSS, "".join(body)))

    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(doc)

    print("리포트 생성 완료: %s" % dst)
    print("PDF로 저장하려면: 브라우저로 열기 -> Ctrl+P (Mac: Cmd+P) -> 대상 'PDF로 저장'")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
