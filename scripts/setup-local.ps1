# Dave 저장소 로컬 PC 설치 스크립트 (Windows PowerShell)
#
# 수행 내용:
#   1) git / node 설치 확인
#   2) Claude Code CLI 설치 (없을 때만)
#   3) %USERPROFILE%\Dave 로 저장소 클론 (없을 때만)
#   4) 작업 브랜치 체크아웃
#
# 사용법: powershell -ExecutionPolicy Bypass -File setup-local.ps1

$ErrorActionPreference = 'Stop'
# 네이티브 명령(git 등)의 0 이 아닌 종료 코드는 직접 검사한다.
$PSNativeCommandUseErrorActionPreference = $false

$RepoUrl   = 'https://github.com/yspark624-bit/Dave.git'
$TargetDir = Join-Path $HOME 'Dave'
$Branch    = 'claude/festive-thompson-k3r7cp'

function Write-Info { param($m) Write-Host "[정보] $m" -ForegroundColor Cyan }
function Write-Ok   { param($m) Write-Host "[완료] $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "[주의] $m" -ForegroundColor Yellow }
function Write-Fail { param($m) Write-Host "[오류] $m" -ForegroundColor Red; exit 1 }

function Test-Cmd { param($n) $null -ne (Get-Command $n -ErrorAction SilentlyContinue) }

# 한글 출력 깨짐 방지
try { chcp 65001 > $null } catch { }

Write-Host ''
Write-Info 'Dave 저장소 로컬 설치를 시작합니다.'
Write-Host ''

# --- 1) 사전 준비물 확인 ---------------------------------------------------
if (-not (Test-Cmd 'git')) {
    Write-Fail 'git 이 설치되어 있지 않습니다. https://git-scm.com/downloads 에서 설치 후 다시 실행하세요.'
}
Write-Ok "git 확인: $(git --version)"

if (Test-Cmd 'node') {
    Write-Ok "node 확인: $(node --version)"
} else {
    Write-Warn 'node 가 없습니다. npm 설치 방식이 필요할 경우 https://nodejs.org 에서 설치하세요.'
}

# --- 2) Claude Code CLI 설치 ----------------------------------------------
if (Test-Cmd 'claude') {
    Write-Ok 'Claude Code 이미 설치됨.'
} else {
    Write-Info 'Claude Code CLI 를 설치합니다...'
    $installed = $false
    try {
        Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression
        $installed = $true
        Write-Ok 'Claude Code 설치 완료.'
    } catch {
        Write-Warn "공식 설치 스크립트 실패: $($_.Exception.Message)"
    }
    if (-not $installed) {
        if (Test-Cmd 'npm') {
            Write-Warn 'npm 으로 재시도합니다.'
            npm install -g '@anthropic-ai/claude-code'
            if ($LASTEXITCODE -ne 0) { Write-Fail 'Claude Code 설치에 실패했습니다.' }
            Write-Ok 'Claude Code 설치 완료 (npm).'
        } else {
            Write-Fail 'Claude Code 설치에 실패했습니다. https://code.claude.com/docs/en/setup 를 참고하세요.'
        }
    }
    Write-Warn "'claude' 명령이 인식되지 않으면 PowerShell 을 닫았다가 다시 여세요."
}

# --- 3) 저장소 클론 --------------------------------------------------------
if (Test-Path (Join-Path $TargetDir '.git')) {
    Write-Ok "저장소가 이미 존재합니다: $TargetDir"
} elseif (Test-Path $TargetDir) {
    Write-Fail "$TargetDir 가 이미 있으나 git 저장소가 아닙니다. 다른 이름으로 옮긴 뒤 다시 실행하세요."
} else {
    Write-Info "저장소를 클론합니다: $TargetDir"
    git clone $RepoUrl $TargetDir
    if ($LASTEXITCODE -ne 0) { Write-Fail '클론에 실패했습니다.' }
    Write-Ok '클론 완료.'
}

# --- 4) 브랜치 체크아웃 ----------------------------------------------------
Set-Location $TargetDir
Write-Info "브랜치를 가져옵니다: $Branch"
git fetch origin
git show-ref --verify --quiet "refs/heads/$Branch"
if ($LASTEXITCODE -eq 0) {
    git checkout $Branch
    git pull origin $Branch
} else {
    git checkout -b $Branch "origin/$Branch"
}
Write-Ok "현재 브랜치: $(git rev-parse --abbrev-ref HEAD)"

# --- 안내 -----------------------------------------------------------------
Write-Host ''
Write-Ok '설치가 끝났습니다.'
Write-Host ''
Write-Host '다음 명령으로 시작하세요:'
Write-Host ''
Write-Host "    cd $TargetDir"
Write-Host '    claude'
Write-Host ''
Write-Host "실행 후 'pwd 찍어줘' 라고 입력했을 때"
Write-Host "$TargetDir 가 나오면 로컬 PC에서 실행 중인 것입니다."
Write-Host ''
