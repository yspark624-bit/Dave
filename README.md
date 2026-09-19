# Dave — Stage 2 모멘텀 투자 에이전트

William O'Neil의 CANSLIM과 Mark Minervini의 트렌드 템플릿으로 미국 주식을
추세추종 관점에서 선별·관리하는 개인 투자 분석 저장소입니다.
시세 수집과 지표 계산은 **로컬에서** 처리해 토큰 소모를 최소화합니다.

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
같은 질문을 MCP로 시세를 받아 처리하면 수십만 토큰이 듭니다.

## 로컬 PC에서 실행해야 하는 이유

`scripts/fetch_bars.py`가 쓰는 무료 시세 소스(Yahoo·Stooq)는 **클라우드(웹) 세션에서
조직 네트워크 정책으로 차단**됩니다(실측 확인). 즉 위 파이프라인은 **내 PC에서만**
동작합니다. 클라우드 세션에서는 시세를 MCP 도구로 받아야 하고, 그 결과가 전부
문맥에 들어가므로 토큰이 수백 배 더 듭니다.

내 PC의 파일(PDF·엑셀 등)을 분석하려는 경우에도 로컬 실행이 필요합니다.

- **[로컬 PC 설치 가이드 (docs/LOCAL_SETUP.md)](docs/LOCAL_SETUP.md)**

빠른 설치:

```bash
# macOS / Linux
bash scripts/setup-local.sh
```

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File scripts\setup-local.ps1
```

## 디렉터리 구조

```
scripts/   fetch_bars.py      무료 일봉 수집 (Yahoo, 표준 라이브러리)
           stage2_screen.py   트렌드 템플릿 + RS 계산, 압축 출력
           make_report.py     한글 HTML 리포트
           run_daily.sh       위 3개를 순서대로 실행
           setup-local.sh     macOS/Linux 로컬 설치 자동화
           setup-local.ps1    Windows 로컬 설치 자동화
memory/    watchlist.txt      감시 종목 (30개 이내)
           lessons.md         누적 교훈 — 판단 전 반드시 읽을 것
           journal/           매매 일지 (YYYY-MM-DD.md)
docs/      TOKEN_COST_GUIDE.md  비용 구조와 절감 규칙
           WORKFLOW.md          매일·매주 루틴
           LOCAL_SETUP.md       로컬 PC 설치 가이드
```

## 문서

| 파일 | 내용 |
|---|---|
| [docs/LOCAL_SETUP.md](docs/LOCAL_SETUP.md) | 로컬 PC 설치·설정, 웹 세션과의 차이 |
| [docs/TOKEN_COST_GUIDE.md](docs/TOKEN_COST_GUIDE.md) | 어떤 작업이 토큰을 먹는가, 절감 규칙 10가지 |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | 매일·매주 루틴, 올바른 AI 호출법 |
| [AGENTS.md](AGENTS.md) | 에이전트 운영 규칙, 폐쇄형 학습 루프 |
| [memory/lessons.md](memory/lessons.md) | 누적된 매매 교훈 |

## 면책

본 저장소의 산출물은 기계적 계산 결과이며 투자 자문이 아닙니다.
투자 판단과 그 결과에 대한 책임은 전적으로 투자자 본인에게 있습니다.
