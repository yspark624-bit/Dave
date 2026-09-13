#!/usr/bin/env python3
"""Stage 2 모멘텀 스크리너 (Minervini 8단계 트렌드 템플릿 + O'Neil RS).

표준 라이브러리만 사용. data/bars/*.csv 를 읽어 로컬에서 전부 계산하고,
사람이(그리고 AI가) 읽을 수 있는 압축 요약만 출력한다.

핵심 목적: 250일치 시세를 AI 문맥에 넣지 않고 결론 한 줄만 남기는 것.
  원시 데이터 1종목 ≈ 15,000 토큰  ->  이 출력 1종목 ≈ 30 토큰

사용법:
    python3 scripts/stage2_screen.py                 # 전체 스크리닝
    python3 scripts/stage2_screen.py --stage2-only   # Stage 2 통과만
    python3 scripts/stage2_screen.py --csv out/screen.csv
"""
import csv
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BARS = os.path.join(ROOT, "data", "bars")
BENCHMARK = "SPY"


# ---------------------------------------------------------------- 지표 계산

def sma(values, period, offset=0):
    """offset봉 전 기준 단순이동평균. 데이터가 모자라면 None."""
    end = len(values) - offset
    start = end - period
    if start < 0:
        return None
    return sum(values[start:end]) / period


def pct(a, b):
    return (a / b - 1.0) * 100.0 if b else 0.0


def rs_score(closes):
    """O'Neil 방식 가중 상대강도 원점수: 최근 분기에 2배 가중."""
    n = len(closes)
    if n < 252:
        return None
    last = closes[-1]
    q = []
    for back in (63, 126, 189, 252):
        q.append(pct(last, closes[n - 1 - back]) if n - 1 - back >= 0 else 0.0)
    return 0.4 * q[0] + 0.2 * q[1] + 0.2 * q[2] + 0.2 * q[3]


def atr_pct(highs, lows, closes, period=20, offset=0):
    """평균 실질 변동폭을 종가 대비 %로. 변동성 수축(VCP) 판정용."""
    end = len(closes) - offset
    start = end - period
    if start < 1:
        return None
    total = 0.0
    for i in range(start, end):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        total += tr
    return (total / period) / closes[end - 1] * 100.0


# ---------------------------------------------------------------- 데이터 적재

def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append((
                    r["date"],
                    float(r["high"]), float(r["low"]),
                    float(r["adjclose"] or r["close"]), float(r["volume"] or 0),
                ))
            except (ValueError, KeyError):
                continue
    return rows


def analyze(ticker, rows):
    dates = [r[0] for r in rows]
    highs = [r[1] for r in rows]
    lows = [r[2] for r in rows]
    closes = [r[3] for r in rows]
    vols = [r[4] for r in rows]

    if len(closes) < 200:
        return None

    price = closes[-1]
    s50, s150, s200 = sma(closes, 50), sma(closes, 150), sma(closes, 200)
    s200_prev = sma(closes, 200, offset=21)   # 1개월(21거래일) 전 200일선
    if None in (s50, s150, s200, s200_prev):
        return None

    window = closes[-252:] if len(closes) >= 252 else closes
    hi52, lo52 = max(window), min(window)

    # --- Minervini 8단계 트렌드 템플릿 ---
    c = {
        "1_주가>150·200MA": price > s150 and price > s200,
        "2_150MA>200MA": s150 > s200,
        "3_200MA_1개월상승": s200 > s200_prev,
        "4_50>150>200MA": s50 > s150 > s200,
        "5_주가>50MA": price > s50,
        "6_저점대비+30%": price >= lo52 * 1.30,
        "7_고점대비-25%내": price >= hi52 * 0.75,
        # 8번(RS>=70)은 유니버스 전체를 봐야 하므로 뒤에서 채운다
    }
    passed = sum(c.values())

    vol50 = sum(vols[-50:]) / 50 if len(vols) >= 50 else 0
    vol10 = sum(vols[-10:]) / 10 if len(vols) >= 10 else 0
    atr_now = atr_pct(highs, lows, closes, 20)
    atr_before = atr_pct(highs, lows, closes, 20, offset=20)

    return {
        "ticker": ticker,
        "date": dates[-1],
        "price": price,
        "criteria": c,
        "passed": passed,
        "sma50": s50, "sma150": s150, "sma200": s200,
        "ext50": pct(price, s50),          # 50일선 이격도 = 진입 타이밍
        "from_high": pct(price, hi52),     # 52주 고점 대비
        "from_low": pct(price, lo52),      # 52주 저점 대비
        "ma200_slope": pct(s200, s200_prev),
        "vol_ratio": (vol10 / vol50) if vol50 else 0,   # 최근 거래량 온도
        "atr_now": atr_now,
        "atr_before": atr_before,
        "rs_raw": rs_score(closes),
        "ret_3m": pct(price, closes[-64]) if len(closes) > 64 else 0,
    }


def classify(m):
    """Weinstein 4국면 분류. Stage 2만 매수 대상."""
    price, s50, s200 = m["price"], m["sma50"], m["sma200"]
    slope = m["ma200_slope"]

    if m["passed"] >= 6 and price > s50 > s200 and slope > 0:
        return "Stage 2"                      # 상승 추세 — 매수/보유
    if price < s200 and s50 < s200 and slope < 0:
        return "Stage 4"                      # 하락 추세 — 회피/청산
    if price > s200 and (price < s50 or slope <= 0):
        return "Stage 3"                      # 천정권 — 보유분 관리
    return "Stage 1"                          # 바닥 다지기 — 관찰


def vcp_flag(m):
    """변동성 수축 + 거래량 감소 = 눌림목 매수 준비 신호."""
    if not (m["atr_now"] and m["atr_before"]):
        return ""
    tight = m["atr_now"] < m["atr_before"] * 0.85
    dry = m["vol_ratio"] < 0.85
    near = m["from_high"] > -12
    if tight and dry and near:
        return "VCP"
    if tight and near:
        return "수축"
    return ""


def account_fit(m, stage):
    """사용자 계좌 구조에 맞춘 배분 제안.

    단기 스윙=Webull / 중기=Roth IRA 2개 / 장기=401k 2개(Principal·Ascensus)
    """
    if stage != "Stage 2":
        return "-"
    if m["rs_pct"] >= 90 and abs(m["ext50"]) < 8 and m["from_high"] > -10:
        return "Webull(스윙)"
    if m["rs_pct"] >= 80 and m["ma200_slope"] > 2:
        return "RothIRA(중기)"
    if m["rs_pct"] >= 70 and m["ma200_slope"] > 0:
        return "401k(장기)"
    return "관찰"


# ---------------------------------------------------------------- 실행

def main(argv):
    stage2_only = "--stage2-only" in argv
    csv_out = None
    if "--csv" in argv:
        csv_out = argv[argv.index("--csv") + 1]

    files = sorted(glob.glob(os.path.join(BARS, "*.csv")))
    if not files:
        print("data/bars/ 가 비었습니다. 먼저 실행: python3 scripts/fetch_bars.py")
        return 1

    metrics = []
    for path in files:
        ticker = os.path.splitext(os.path.basename(path))[0]
        m = analyze(ticker, load(path))
        if m:
            metrics.append(m)

    if not metrics:
        print("분석 가능한 종목이 없습니다(200봉 이상 필요).")
        return 1

    # RS 백분위(1~99) — 유니버스 내 순위. 이것이 트렌드 템플릿 8번 조건.
    scored = [m for m in metrics if m["rs_raw"] is not None]
    scored.sort(key=lambda m: m["rs_raw"])
    for i, m in enumerate(scored):
        m["rs_pct"] = int(round(1 + 98 * i / max(1, len(scored) - 1)))
    for m in metrics:
        m.setdefault("rs_pct", 0)
        m["criteria"]["8_RS>=70"] = m["rs_pct"] >= 70
        m["passed"] = sum(m["criteria"].values())
        m["stage"] = classify(m)
        m["vcp"] = vcp_flag(m)
        m["fit"] = account_fit(m, m["stage"])

    bench = next((m for m in metrics if m["ticker"] == BENCHMARK), None)
    metrics.sort(key=lambda m: (m["stage"] != "Stage 2", -m["rs_pct"]))

    # ---- 시장 국면 (O'Neil: 시장 방향이 M — 가장 중요) ----
    print("=" * 78)
    if bench:
        state = "상승(매수 가능)" if bench["price"] > bench["sma200"] and bench["ma200_slope"] > 0 else "주의(현금 비중 확대)"
        print("시장 국면  %s  |  SPY %.2f  200MA대비 %+.1f%%  200MA기울기 %+.2f%%/월  ->  %s"
              % (bench["date"], bench["price"], pct(bench["price"], bench["sma200"]), bench["ma200_slope"], state))
    print("=" * 78)

    hdr = "%-6s %-8s %3s %4s %7s %7s %7s %7s %5s %-13s" % (
        "종목", "국면", "TT", "RS", "주가", "50MA%", "고점%", "3M%", "신호", "계좌")
    print(hdr)
    print("-" * 78)

    shown = 0
    for m in metrics:
        if m["ticker"] == BENCHMARK:
            continue
        if stage2_only and m["stage"] != "Stage 2":
            continue
        print("%-6s %-8s %d/8 %4d %7.2f %+6.1f%% %+6.1f%% %+6.1f%% %5s %-13s" % (
            m["ticker"], m["stage"], m["passed"], m["rs_pct"], m["price"],
            m["ext50"], m["from_high"], m["ret_3m"], m["vcp"], m["fit"]))
        shown += 1

    print("-" * 78)
    n2 = sum(1 for m in metrics if m["stage"] == "Stage 2" and m["ticker"] != BENCHMARK)
    print("총 %d종목 표시 | Stage 2: %d종목 | TT=트렌드템플릿 통과수, RS=상대강도 백분위" % (shown, n2))
    print("매수 후보 기준: Stage 2 + TT 7/8 이상 + RS 80 이상 + 50MA 이격 +5% 이내")

    if csv_out:
        os.makedirs(os.path.dirname(csv_out) or ".", exist_ok=True)
        with open(csv_out, "w", newline="", encoding="utf-8") as fh:
            cols = ["ticker", "date", "stage", "passed", "rs_pct", "price", "ext50",
                    "from_high", "from_low", "ma200_slope", "vol_ratio", "ret_3m", "vcp", "fit"]
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(metrics)
        print("\n상세 CSV 저장: %s" % csv_out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
