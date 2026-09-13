#!/usr/bin/env bash
# 매일 장 마감 후 실행하는 전체 파이프라인 (토큰 소모 0)
#   사용법: bash scripts/run_daily.sh
set -euo pipefail

cd "$(dirname "$0")/.."
PY="${PYTHON:-python3}"

echo "[1/3] 무료 시세 수집 중..."
"$PY" scripts/fetch_bars.py

echo
echo "[2/3] Stage 2 스크리닝 (로컬 계산)..."
"$PY" scripts/stage2_screen.py --csv out/screen.csv

echo
echo "[3/3] 한글 리포트 생성..."
"$PY" scripts/make_report.py out/screen.csv out/report.html

echo
echo "────────────────────────────────────────────────────────────"
echo "완료. 위 표를 복사해 AI에게 붙여넣고 질문하세요 (약 500토큰)."
echo "PDF: out/report.html 을 브라우저로 열고 Ctrl+P -> PDF로 저장"
echo "────────────────────────────────────────────────────────────"
