# Dave — Stage 2 모멘텀 투자 에이전트

토큰을 거의 쓰지 않고 매일 돌릴 수 있는 추세추종 주식 스크리닝 파이프라인입니다.
William O'Neil의 CANSLIM과 Mark Minervini의 트렌드 템플릿을 **로컬에서** 계산합니다.

## 빠른 시작

```bash
# 1. 감시 종목 설정
vi memory/watchlist.txt

# 2. 매일 장 마감 후 실행 (약 2분, 토큰 0원)
bash scripts/run_daily.sh
```

설치할 패키지가 없습니다. 파이썬 3.8 이상이면 표준 라이브러리만으로 동작합니다.

## 출력 예시

```
시장 국면  2026-09-12 | SPY 612.40  200MA대비 +7.2%  기울기 +1.1%/월 -> 상승(매수 가능)
종목   국면      TT   RS     주가   50MA%   고점%    3M%   신호  계좌
NVDA  Stage 2  8/8   96   184.20  +3.1%   -2.4%  +22.1%  VCP  Webull(스윙)
AVGO  Stage 2  7/8   88   342.10  +6.8%   -7.1%  +14.0%       RothIRA(중기)
```

이 표를 복사해 AI에게 붙여넣고 질문하면 **1회당 약 500토큰**입니다.
산출물은 터미널 표가 기본입니다. PDF를 만들거나 메일·Notion으로 보내지 않습니다.
같은 질문을 MCP로 시세를 받아 처리하면 약 750,000토큰이 듭니다.

## 문서

| 파일 | 내용 |
|---|---|
| [docs/TOKEN_COST_GUIDE.md](docs/TOKEN_COST_GUIDE.md) | 어떤 작업이 토큰을 먹는가, 절감 규칙 10가지 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | 매일·매주 루틴, 올바른 AI 호출법 |
| [AGENTS.md](AGENTS.md) | 에이전트 운영 규칙, 폐쇄형 학습 루프 |
| [memory/lessons.md](memory/lessons.md) | 누적된 매매 교훈 |

## 면책

본 저장소의 산출물은 기계적 계산 결과이며 투자 자문이 아닙니다.
투자 판단과 그 결과에 대한 책임은 전적으로 투자자 본인에게 있습니다.
