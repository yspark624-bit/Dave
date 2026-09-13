# Dave

Stage 2 추세추종 기반 투자 분석 에이전트 저장소.
[Hermes-Agent](https://github.com/NousResearch/hermes-agent)의 폐쇄형 학습 루프 원칙을
Claude Code 환경에 맞게 옮긴 구조다.

## 구조

```
CLAUDE.md              매 세션 자동 로딩 — 얇게 유지 (30줄)
profile/
  accounts.md          계좌 5개의 성격·보유기간·배정 원칙
  rules.md             추세 템플릿 8항목, CANSLIM, 리스크 기준
journal/
  TEMPLATE.md          판정 기록 양식 (채점란 포함)
  YYYY/MM/*.md         날짜별 원본 기록
memory/
  watchlist.md         추적 종목 — 세션 시작 시 자동 주입
reports/               PDF 산출물
.claude/
  hooks/session-start.sh   메모리 주입 (Hermes의 memory nudge)
  settings.json            훅 등록 + Webull 읽기 도구 허용
```

## 학습 루프

현재 **① 실행 → ② 관찰** 단계까지 구현돼 있다.

1. **실행** — 종목 판정 시 `journal/`에 당시 가격·근거를 기록
2. **관찰** — 몇 주 뒤 실제 결과를 채점란에 기입
3. 증류 — *(미구현)* 반복 패턴을 규칙으로 승격
4. 반영 — *(미구현)* 규칙을 스킬 파일에 반영

기록이 쌓이면 ③④를 추가한다.

## 원칙

- 판정 당시 가격과 근거를 반드시 남긴다. 나중에 채점할 수 없으면 루프가 죽는다.
- 결과를 알고 난 뒤 과거 기록을 고쳐 쓰지 않는다.
- `memory/watchlist.md`가 길어지면 정리한다. 매 세션 문맥에 들어가는 비용이다.
- 원격 컨테이너는 일회성이므로 반드시 커밋·푸시한다.
