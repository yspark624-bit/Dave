#!/usr/bin/env python3
"""무료 일봉 수집기 (표준 라이브러리만 사용, 설치 불필요).

Yahoo Finance 공개 chart API에서 일봉을 받아 data/bars/<TICKER>.csv 로 저장한다.
토큰 비용 0원 — 사용자 PC에서 직접 실행하는 용도.

사용법:
    python3 scripts/fetch_bars.py                    # watchlist.txt 전체
    python3 scripts/fetch_bars.py NVDA AVGO SPY      # 특정 종목만
    python3 scripts/fetch_bars.py --range 2y
"""
import csv
import json
import os
import ssl
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "data", "bars")
WATCHLIST = os.path.join(ROOT, "memory", "watchlist.txt")
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{t}?range={r}&interval=1d"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"


def read_watchlist():
    if not os.path.exists(WATCHLIST):
        return []
    out = []
    with open(WATCHLIST, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#")[0].strip().upper()
            if line:
                out.append(line)
    return out


def fetch(ticker, rng):
    req = urllib.request.Request(URL.format(t=ticker, r=rng), headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        payload = json.load(resp)

    result = payload["chart"]["result"][0]
    stamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    adj = result["indicators"].get("adjclose", [{}])[0].get("adjclose") or quote["close"]

    rows = []
    for i, ts in enumerate(stamps):
        c = quote["close"][i]
        if c is None:
            continue
        rows.append({
            "date": time.strftime("%Y-%m-%d", time.gmtime(ts)),
            "open": quote["open"][i],
            "high": quote["high"][i],
            "low": quote["low"][i],
            "close": c,
            "adjclose": adj[i] if adj[i] is not None else c,
            "volume": quote["volume"][i] or 0,
        })
    return rows


def save(ticker, rows):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, ticker + ".csv")
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "open", "high", "low", "close", "adjclose", "volume"])
        w.writeheader()
        w.writerows(rows)
    return path


def main(argv):
    rng = "2y"
    tickers = []
    i = 0
    while i < len(argv):
        if argv[i] == "--range":
            rng = argv[i + 1]
            i += 2
            continue
        tickers.append(argv[i].upper())
        i += 1

    if not tickers:
        tickers = read_watchlist()
    if not tickers:
        print("감시 종목이 없습니다. memory/watchlist.txt 에 티커를 추가하세요.")
        return 1
    if "SPY" not in tickers:
        tickers.append("SPY")  # RS 계산용 벤치마크

    ok = err = 0
    for t in tickers:
        try:
            rows = fetch(t, rng)
            if len(rows) < 60:
                print("  [건너뜀] %-6s 데이터 부족 (%d봉)" % (t, len(rows)))
                err += 1
                continue
            save(t, rows)
            print("  [저장] %-6s %d봉  최종 %s  종가 %.2f" % (t, len(rows), rows[-1]["date"], rows[-1]["close"]))
            ok += 1
        except Exception as exc:  # noqa: BLE001 - 한 종목 실패가 전체를 막지 않도록
            print("  [실패] %-6s %s" % (t, exc))
            err += 1
        time.sleep(0.4)  # 무료 API 예의상 간격

    print("\n완료: 성공 %d / 실패 %d  ->  data/bars/" % (ok, err))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
