# 로컬 PC에서 Dave 저장소 작업하기

이 문서는 **웹(클라우드) 세션이 아니라 내 PC에서** Claude Code로 이 저장소를
작업하기 위한 설치·설정 가이드입니다.

---

## 왜 로컬 PC가 필요한가

| 항목 | 웹(클라우드) 세션 | 로컬 PC |
|---|---|---|
| 실행 위치 | Anthropic 관리 컨테이너 | 내 PC |
| 작업 경로 | `/home/user/Dave` (임시) | `~/Dave` (영구) |
| 내 PC 파일 접근 | 불가 | **가능** |
| 세션 종료 후 | 컨테이너 회수(삭제) | 그대로 남음 |
| 푸시 안 한 변경 | **소실됨** | 유지됨 |

> PDF·엑셀 등 **내 PC에 있는 파일을 분석**하려면 로컬 PC 실행이 필요합니다.

---

## 1단계. 사전 준비물

- **Git** — https://git-scm.com/downloads
- **Node.js 18 이상** (npm 설치 방식을 쓸 경우) — https://nodejs.org
- **Claude 계정** (Pro / Max / Team, 또는 Anthropic API 키)

설치 확인:

```bash
git --version
node --version
```

---

## 2단계. Claude Code CLI 설치

### macOS / Linux

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://claude.ai/install.ps1 | iex
```

### 공통 대안 (npm)

```bash
npm install -g @anthropic-ai/claude-code
```

설치 확인:

```bash
claude --version
```

> `claude: command not found` 가 나오면 터미널을 완전히 닫았다가 다시 여세요.
> PATH 갱신이 새 터미널에서만 반영됩니다.

---

## 3단계. 저장소 클론

### macOS / Linux

```bash
cd ~
git clone https://github.com/yspark624-bit/Dave.git Dave
cd ~/Dave
```

### Windows (PowerShell)

```powershell
cd $HOME
git clone https://github.com/yspark624-bit/Dave.git Dave
cd $HOME\Dave
```

---

## 4단계. 작업 브랜치 체크아웃

웹 세션에서 쓰는 브랜치와 동일하게 맞춥니다.

```bash
git fetch origin
git checkout claude/festive-thompson-k3r7cp
```

---

## 5단계. Claude Code 실행

```bash
cd ~/Dave
claude
```

최초 실행 시 브라우저가 열리며 로그인(인증)을 진행합니다.
로그인 후 프롬프트에서 바로 작업을 지시하면 됩니다.

실행 후 확인:

```
> pwd 찍어줘
```

`/Users/내이름/Dave` 또는 `C:\Users\내이름\Dave` 가 나오면 **로컬 PC에서 실행 중**입니다.
`/home/user/Dave` 가 나오면 여전히 웹 세션입니다.

---

## 자동 설치 스크립트

수동 단계가 번거로우면 아래 스크립트를 쓰세요.
(스크립트는 Git·Node 확인 → Claude Code 설치 → 클론 → 브랜치 체크아웃까지 수행)

### macOS / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/yspark624-bit/Dave/claude/festive-thompson-k3r7cp/scripts/setup-local.sh -o setup-local.sh
less setup-local.sh          # 내용 확인 후 실행 권장
bash setup-local.sh
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/yspark624-bit/Dave/claude/festive-thompson-k3r7cp/scripts/setup-local.ps1 -OutFile setup-local.ps1
notepad setup-local.ps1      # 내용 확인 후 실행 권장
powershell -ExecutionPolicy Bypass -File setup-local.ps1
```

---

## 일상 작업 흐름

```bash
cd ~/Dave
git pull origin claude/festive-thompson-k3r7cp   # 웹 세션 변경분 받기
claude                                            # 작업
git add -A
git commit -m "작업 내용"
git push -u origin claude/festive-thompson-k3r7cp
```

**웹 ↔ 로컬을 오갈 때는 반드시 작업 전 `git pull`, 작업 후 `git push`** 를 하세요.
그래야 양쪽이 같은 내용을 봅니다.

---

## 자주 겪는 문제

| 증상 | 해결 |
|---|---|
| `claude: command not found` | 터미널 재시작. 그래도 안 되면 `npm install -g @anthropic-ai/claude-code` |
| 클론 시 인증 요구 | GitHub 로그인 필요. 비밀번호 대신 **Personal Access Token** 사용 |
| `Permission denied (publickey)` | HTTPS URL 사용 권장 (위 명령 그대로) |
| 푸시 거부 (non-fast-forward) | `git pull --rebase origin claude/festive-thompson-k3r7cp` 후 재푸시 |
| 한글 깨짐 (Windows) | PowerShell에서 `chcp 65001` 실행 |

---

## 참고 문서

- Claude Code 설치: https://code.claude.com/docs/en/setup
- Claude Code on the web: https://code.claude.com/docs/en/claude-code-on-the-web
