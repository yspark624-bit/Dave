#!/bin/bash
# Dave 에이전트 — 세션 시작 시 메모리 주입 (Hermes-Agent의 "memory nudge")
# 출력이 그대로 세션 문맥에 들어가므로, 토큰 비용을 위해 분량을 제한한다.
set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

echo "=== Dave 에이전트 메모리 ==="
echo "오늘: $(date +%Y-%m-%d)"
echo

if [ -s memory/watchlist.md ]; then
  echo "--- 워치리스트 (memory/watchlist.md) ---"
  head -n 25 memory/watchlist.md
  echo
fi

latest=$(find journal -type f -name '20*.md' 2>/dev/null | sort | tail -n 1)
if [ -n "${latest:-}" ]; then
  echo "--- 최근 기록: $latest ---"
  head -n 25 "$latest"
  echo "  (전체 내용은 필요할 때 직접 읽을 것)"
  echo
fi

echo "--- 기록 의무 ---"
echo "종목 판정/매매 검토를 하면 journal/$(date +%Y/%m)/$(date +%Y-%m-%d).md 에"
echo "기록하고(형식: journal/TEMPLATE.md), memory/watchlist.md 를 갱신한 뒤 커밋·푸시할 것."
exit 0
