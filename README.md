## pytest 평소 실행
> pytest

## slow marker만 실행
> pytest -m slow 

## 브라우저별 실행

- Firefox
> pytest

- Chrome
> pytest --browser chrome

## Jira Issue Report 생성 (임시)
> pytest --jira

## pytest-xdist (pytest 병렬 실행)
### pytest-xdist 설치
> pip install pytest-xdist

### 기본 사용법
1. CPU 개수만큼 자동 병렬 실행
> pytest -n auto

--> auto 사용 시 논리 프로세스 수로 워커 생성되어 과부하 발생 가능성 높아짐
--> 아래 스텝으로 진행

1. 본인 CPU 코어 수 확인 wmic cpu get NumberOfCores
2. 코어 수에 맞게 실행pytest -n <코어수> --dist=loadfile

=> 브라우저 과다 실행으로 TimeoutException, 세션 충돌 에러 증가 가능성 있음

2. 직접 프로세스 개수 지정
> pytest -n 4


## Allure 리포트 환경 설정
### Allure 설치 순서
#### 사전 준비

* Scoop 없는 경우 먼저 설치 @powershell
> Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
> irm get.scoop.sh | iex


1. Java 설치 (Allure 실행에 필요) - scoop 사용
> scoop bucket add java
> scoop install temurin-lts

-- temurin-lts 실행 불가시
> scoop search temurin
temurin-lts 혹은 temurin-lts-jdk로 설치

-- 자바 설치 확인
> java -version
: openjdk version "25..." 출력되면 성공

2. Python 패키지 설치
VS Code 터미널에서 우측 상단 + 옆 드롭다운 → PowerShell 선택
> pip install allure-pytest

3. Allure CLI 설치
> scoop install allure

4. 설치 확인
> java -version
> allure --version
> pip show allure-pytest

* Scoop 설치 시 팝업이 뜨면 Yes 또는 A(모두 허용) 선택


## Allure 리포트 확인
테스트 실행 후 allure-report/ 가 자동 생성됩니다.

### 브라우저로 바로 열기
> allure serve allure-results

### 정적 리포트 생성 후 열기
> allure open allure-report


## Allure 리포트 확인 없이 테스트만 실행
> pytest tests/ --no-header -p no:allure

# 🤖 Focus - Helpy Chat QA 자동화 프로젝트

> AI 교육 플랫폼 **Helpy Chat** 서비스의 E2E 테스트 자동화 및 CI/CD 파이프라인 구축 프로젝트

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 테스트 대상 | Helpy Chat (AI 기반 교육 도우미 서비스) |
| 역할 | Settings/Tools 테스트 자동화, CI/CD 파이프라인 구축 |
| 기간 | 2025 |
| 비고 | 팀 프로젝트 참여 후 개인 포트폴리오로 전환하여 지속 개발 중 |

---

## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| 테스트 프레임워크 | pytest, Selenium |
| 리포트 | Allure Report |
| CI/CD | GitLab CI/CD → GitHub Actions |
| 알림 | Discord Webhook |
| 이슈 관리 | Jira |

---

## 📁 프로젝트 구조

focus/
├── config/                  # 브라우저, 설정, 로그인 헬퍼
│   ├── browser_factory.py   # Firefox/Chrome 드라이버 생성
│   ├── settings.py          # URL, 타임아웃, 테스트 계정 설정
│   ├── login_helpers.py     # 공통 로그인/배너 처리
│   └── requirements.txt     # 의존성 패키지
├── pages/                   # Page Object Model
│   ├── base_page.py
│   ├── tools/               # Tools 페이지 객체
│   ├── settings/            # Settings 페이지 객체
│   ├── agents/              # Agents 페이지 객체
│   └── mypage/              # 마이페이지 객체
├── tests/                   # 테스트 코드
│   ├── login/
│   ├── logout/
│   ├── signup/
│   ├── chat/
│   ├── tools/               # ✅ 담당
│   ├── settings/            # ✅ 담당
│   ├── agent/
│   ├── mypage/
│   └── performance/
├── scripts/
│   ├── ci_allure.py         # Allure 리포트 생성 스크립트
│   └── ci_notify.py         # Discord 알림 스크립트
├── .github/workflows/
│   └── ci.yml               # GitHub Actions 워크플로우
├── conftest.py              # 공통 fixture 및 Jira 연동 훅
└── pytest.ini

---

## ⚙️ CI/CD 파이프라인

GitHub Actions를 통해 `main`, `develop` 브랜치 push 시 자동 실행됩니다.
push → 테스트 실행 (pytest)
→ Allure 리포트 생성 (GitHub Pages 배포)
→ Discord 알림 전송

### 파이프라인 구성

| 단계 | 내용 |
|------|------|
| `run_tests` | pytest로 전체 테스트 실행, 결과를 아티팩트로 저장 |
| `pages` | Allure 리포트 생성 후 GitHub Pages에 배포 |
| `notify_discord` | 테스트 결과 Discord 채널에 알림 전송 |

---

## 🧪 테스트 범위

| 영역 | 테스트 항목 |
|------|------------|
| 로그인/로그아웃 | 정상 로그인, 유효성 검사, 계정 잠금 |
| 회원가입 | 필수/전체 항목 가입, 유효성 검사 |
| 채팅 | 새 채팅, AI 응답, 검색, 채팅 목록 |
| Tools ✅ | 전문성 분석, 행동 분석, 수업지도안, PPT, 퀴즈, 심층조사 |
| Settings ✅ | 일반, 사용량, 모델, 구독, 구성원, 기관 설정 |
| Agents | 에이전트 탭, 기능 표시, 채팅 연동 |
| 마이페이지 | 프로필, 계정, 언어, 기관, 탈퇴 |
| 성능 | 부하 테스트 (FHC-094~099) |

---

## 🚀 로컬 실행 방법

### 1. 환경변수 설정

`.env.example`을 복사해 `.env` 파일 생성 후 값 입력:

```bash
cp .env.example .env
```

```env
JIRA_URL=https://your-domain.atlassian.net/
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=YOUR_KEY
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### 2. 패키지 설치

```bash
pip install -r config/requirements.txt
```

### 3. 테스트 실행

```bash
# 전체 실행
python -m pytest tests/ -v

# 특정 영역만 실행
python -m pytest tests/settings/ -v
python -m pytest tests/tools/ -v

# slow/xfail 제외 실행
python -m pytest tests/ -m "not slow and not xfail" -v
```

---

## 📊 Allure 리포트

```bash
# 리포트 생성
allure generate allure-results -o allure-report --clean

# 리포트 열기
allure open allure-report
```

---

## 🔐 환경변수 목록

| 변수명 | 설명 |
|--------|------|
| `JIRA_URL` | Jira 인스턴스 URL |
| `JIRA_EMAIL` | Jira 계정 이메일 |
| `JIRA_API_TOKEN` | Jira API 토큰 |
| `JIRA_PROJECT_KEY` | Jira 프로젝트 키 |
| `DISCORD_WEBHOOK_URL` | Discord 웹훅 URL |
| `TEST_USER_ID` | 테스트 계정 이메일 (선택) |
| `TEST_USER_PW` | 테스트 계정 비밀번호 (선택) |