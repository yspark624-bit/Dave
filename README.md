# Dave

개인 투자 분석 및 에이전트 작업용 저장소.

## 로컬 PC에서 작업하기

내 PC의 파일(PDF, 엑셀 등)을 분석하려면 웹 세션이 아니라 **로컬 PC**에서
Claude Code 를 실행해야 합니다. 설치 방법은 아래 문서를 참고하세요.

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
docs/     문서
scripts/  설치 및 유틸리티 스크립트
```
