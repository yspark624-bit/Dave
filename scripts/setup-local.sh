#!/usr/bin/env bash
# Dave 저장소 로컬 PC 설치 스크립트 (macOS / Linux)
#
# 수행 내용:
#   1) git / node 설치 확인
#   2) Claude Code CLI 설치 (없을 때만)
#   3) ~/Dave 로 저장소 클론 (없을 때만)
#   4) 작업 브랜치 체크아웃
#
# 사용법: bash setup-local.sh

set -euo pipefail

REPO_URL="https://github.com/yspark624-bit/Dave.git"
TARGET_DIR="${HOME}/Dave"
BRANCH="claude/festive-thompson-k3r7cp"

info()  { printf '\033[1;34m[정보]\033[0m %s\n' "$*"; }
ok()    { printf '\033[1;32m[완료]\033[0m %s\n' "$*"; }
warn()  { printf '\033[1;33m[주의]\033[0m %s\n' "$*"; }
fail()  { printf '\033[1;31m[오류]\033[0m %s\n' "$*" >&2; exit 1; }

echo
info "Dave 저장소 로컬 설치를 시작합니다."
echo

# --- 1) 사전 준비물 확인 ---------------------------------------------------
command -v git >/dev/null 2>&1 || fail "git 이 설치되어 있지 않습니다. https://git-scm.com/downloads 에서 설치 후 다시 실행하세요."
ok "git 확인: $(git --version)"

if command -v node >/dev/null 2>&1; then
  ok "node 확인: $(node --version)"
else
  warn "node 가 없습니다. npm 설치 방식이 필요할 경우 https://nodejs.org 에서 설치하세요."
fi

# --- 2) Claude Code CLI 설치 ----------------------------------------------
if command -v claude >/dev/null 2>&1; then
  ok "Claude Code 이미 설치됨: $(claude --version 2>/dev/null || echo '버전 확인 실패')"
else
  info "Claude Code CLI 를 설치합니다..."
  if curl -fsSL https://claude.ai/install.sh | bash; then
    ok "Claude Code 설치 완료."
  elif command -v npm >/dev/null 2>&1; then
    warn "공식 설치 스크립트 실패. npm 으로 재시도합니다."
    npm install -g @anthropic-ai/claude-code || fail "Claude Code 설치에 실패했습니다."
    ok "Claude Code 설치 완료 (npm)."
  else
    fail "Claude Code 설치에 실패했습니다. https://code.claude.com/docs/en/setup 를 참고하세요."
  fi
  warn "'claude' 명령이 인식되지 않으면 터미널을 닫았다가 다시 여세요."
fi

# --- 3) 저장소 클론 --------------------------------------------------------
if [ -d "${TARGET_DIR}/.git" ]; then
  ok "저장소가 이미 존재합니다: ${TARGET_DIR}"
elif [ -e "${TARGET_DIR}" ]; then
  fail "${TARGET_DIR} 가 이미 있으나 git 저장소가 아닙니다. 다른 이름으로 옮긴 뒤 다시 실행하세요."
else
  info "저장소를 클론합니다: ${TARGET_DIR}"
  git clone "${REPO_URL}" "${TARGET_DIR}"
  ok "클론 완료."
fi

# --- 4) 브랜치 체크아웃 ----------------------------------------------------
cd "${TARGET_DIR}"
info "브랜치를 가져옵니다: ${BRANCH}"
git fetch origin
if git show-ref --verify --quiet "refs/heads/${BRANCH}"; then
  git checkout "${BRANCH}"
  git pull origin "${BRANCH}"
else
  git checkout -b "${BRANCH}" "origin/${BRANCH}"
fi
ok "현재 브랜치: $(git rev-parse --abbrev-ref HEAD)"

# --- 안내 -----------------------------------------------------------------
echo
ok "설치가 끝났습니다."
echo
echo "다음 명령으로 시작하세요:"
echo
echo "    cd ${TARGET_DIR}"
echo "    claude"
echo
echo "실행 후 'pwd 찍어줘' 라고 입력했을 때"
echo "${TARGET_DIR} 가 나오면 로컬 PC에서 실행 중인 것입니다."
echo
