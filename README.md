# 🤖 AI Helpy Chat QA 자동화 프로젝트 (Focus)

> 기업용 AI 통합 플랫폼 **Helpy Chat**의 핵심 기능 품질 검증 및 E2E 테스트 자동화 구축
> *팀 프로젝트 진행 후, 개인 포트폴리오로 전환하여 지속 개발 중*

<!-- TODO: 코드/스크린샷 확정 후 채울 항목은 "TODO" 검색으로 일괄 처리 -->

---

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 대상 서비스 | AI Helpy Chat (GPT · Gemini · Claude 등 다양한 AI 모델을 제공하는 기업용 플랫폼) |
| 진행 기간 | 2025.05.13 ~ 2025.06.01 (약 3주) |
| 팀명 | Focus |
| 인원 | 4명 |
| 목표 | 핵심 기능 품질 검증 · 반복 테스트 자동화 · 테스트 안정성 및 유지보수 강화 |

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| 자동화 | pytest, Selenium |
| 구조 설계 | Page Object Model (POM) |
| CI/CD | GitLab CI/CD *(팀 프로젝트)* → GitHub Actions *(개인 포트폴리오 전환)* |
| 리포팅 | Allure Report |
| 이슈 관리 | Jira (테스트 실패 시 자동 등록) |
| 알림 | Discord Webhook |
| 협업 | Notion, GitLab MR, Daily Scrum |

---

## 👩‍💻 나의 역할

- **Settings / Tools (lesson, ppt 등) 자동화 테스트 구현**
- **Allure 리포트 연동 및 시각화** — 테스트 실행 결과 회차별 그래프 추적
- **CI/CD 파이프라인 구축 및 운영** — 3단계 파이프라인 설계 (Test → Deploy → Notify)
- **Discord Webhook 연동** — 테스트 결과 자동 알림 구현 (브랜치·커밋·담당자·성공/실패 건수·Allure 링크 포함)

---

## 📊 테스트 성과

| 지표 | 결과 |
|------|------|
| 총 테스트 케이스 수 | **58개** |
| 테스트 실행 시간 단축률 | **48.1%** (약 1.93배 성능 개선) |
| 전체 테스트 실행 시간 | 약 46분 → **23분** |
| 로그인 횟수 절감 | 57회 → 23회 (**34회 감소**) |
| setup 시간 절감 | 628초 → 253초 (**374초, 약 6분 14초 단축**) |
| POM 도입 후 유지보수 효율 | 수정 파일 수 최대 **96.6% 절감** |

<!-- TODO: Allure 리포트 그래프 스크린샷 추가
     allure serve 로 리포트 띄운 뒤 캡처 → docs/ 폴더에 저장 후 아래처럼 삽입
     (주의: images/ 폴더는 테스트 픽스처용이므로 스크린샷을 섞지 말 것)
![Allure Report](./docs/allure-report.png)
-->

---

## 🏗️ 시스템 구조

### CI/CD 파이프라인
`main` · `develop` 브랜치 push 시 자동 트리거

```
Stage 1: Test     → 테스트 케이스 자동 실행 + Jira 버그 자동 등록
Stage 2: Deploy   → Allure 리포트 생성 → GitHub Pages 배포
Stage 3: Notify   → Discord 채널에 결과 알림 발송
```

### POM 3계층 구조

```
1계층  BasePage      → 클릭·입력·대기 등 브라우저 공통 동작 정의
2계층  기능별 Page    → 페이지 이동·언어 변경 등 도메인별 공유 로직
3계층  세부 Page      → 로케이터와 세부 동작 캡슐화
```

> 테스트 코드엔 **"무엇을 검증할지"만 남는 구조**.
> UI·로케이터가 바뀌어도 해당 Page 파일 하나만 수정하면 됩니다.

---

## ✅ 테스트 범위

| 영역 | 테스트 항목 |
|------|------------|
| 로그인 / 로그아웃 / 회원가입 | 정상 로그인, 유효성 검사, 계정 잠금, 필수/전체 항목 가입 |
| 채팅 | 새 채팅, AI 응답, 검색, 채팅 목록 |
| **Tools** ✅ *(담당)* | 전문성 분석, 행동 분석, 수업지도안(lesson), PPT, 퀴즈 생성, 심층조사 |
| **Settings** ✅ *(담당)* | 일반, 사용량, 모델, 구독, 구성원, 기관 설정 |
| Agents | 에이전트 탭, 기능 표시, 채팅 연동 |
| 마이페이지 | 프로필, 계정, 언어, 내 기관, 고객센터, 탈퇴 |
| 성능 | 부하 테스트 (FHC-094~099) |
| 크로스 브라우저 | Edge · Chrome |

---

## 🐛 주요 문제 해결 경험

**1. 계정 탈퇴 후 재가입 경로 불일치**
탈퇴 후 서버가 `signup/method`로 강제 리다이렉트하여 기존 경로 탐색 실패
→ `signup/method` 직접 접근 방식으로 변경

**2. 테스트 실패 시 파이프라인 후속 job 스킵 문제**
CI 기본 동작으로 이전 stage 실패 시 이후 job 전체 스킵
→ `when: always` 설정으로 리포트·알림 job 항상 실행

**3. Chrome 크로스 브라우저 호환성**
Chrome에서 입력값 누적 및 브라우저 상태 공유 문제 발생
→ JavaScript 직접 입력 처리 + 테스트마다 브라우저 새로 초기화

**4. Jira 자동 등록 Hook 구조 개선**
Jira 생성 Hook이 특정 fixture에 종속되어 공통 동작 불가
→ Driver 기반 공통 Hook 구조로 전환

---

## 📁 프로젝트 구조

```
focus/
├── config/                   # 브라우저·설정·로그인 헬퍼
│   ├── browser_factory.py    # Edge/Chrome 드라이버 생성
│   ├── settings.py           # URL·타임아웃·테스트 계정 설정
│   ├── login_helpers.py      # 공통 로그인/배너 처리
│   ├── jira_config.py        # Jira 연동 설정
│   └── requirements.txt      # 의존성 패키지
├── pages/                    # Page Object Model
│   ├── base_page.py          # 1계층: 공통 동작
│   ├── tools/                # 3계층: Tools 세부 Page
│   ├── settings/             # 3계층: Settings 세부 Page
│   ├── agents/               # Agents Page
│   └── mypage/               # 마이페이지 Page
├── tests/                    # 테스트 코드
│   ├── login/  logout/  signup/  chat/
│   ├── tools/                # ✅ 담당
│   ├── settings/             # ✅ 담당
│   ├── agent/  mypage/  performance/
├── scripts/
│   ├── ci_allure.py          # Allure 리포트 생성 스크립트
│   └── ci_notify.py          # Discord 알림 스크립트
├── .github/workflows/
│   └── test.yml              # GitHub Actions 워크플로우
├── conftest.py               # 공통 fixture 및 Jira 연동 훅
└── pytest.ini
```

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

# 브라우저 지정 (기본 Edge)
python -m pytest --browser chrome
```

### 4. Allure 리포트 확인
```bash
# 실행 후 브라우저로 바로 열기
allure serve allure-results

# 정적 리포트 생성 후 열기
allure generate allure-results -o allure-report --clean
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

---

<details>
<summary>🧰 개발용 명령어 메모 (Allure 설치 · 병렬 실행 등)</summary>

### 병렬 실행 (pytest-xdist)
```bash
pip install pytest-xdist
pytest -n 4 --dist=loadfile     # 코어 수에 맞게 지정 권장
```
> `-n auto`는 논리 프로세서 수만큼 워커를 생성해 과부하·세션 충돌 위험이 있어, 코어 수에 맞춘 직접 지정을 권장.

### Allure 설치 (Windows / Scoop)
```powershell
# Scoop 미설치 시
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Java (Allure 실행에 필요)
scoop bucket add java
scoop install temurin-lts        # 실행 불가 시 temurin-lts-jdk

# Allure CLI + Python 패키지
scoop install allure
pip install allure-pytest

# 설치 확인
java -version
allure --version
pip show allure-pytest
```

### 기타
```bash
pytest -m slow                       # slow marker만 실행
pytest --jira                        # Jira Issue Report 생성
pytest tests/ --no-header -p no:allure   # Allure 없이 테스트만 실행
```

</details>
