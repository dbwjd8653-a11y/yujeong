# 🤖 AI Helpy Chat QA 자동화 프로젝트 (Focus)

> 기업용 AI 통합 플랫폼 **Helpy Chat**의 핵심 기능 품질 검증 및 E2E 테스트 자동화 구축
> *팀 프로젝트 진행 후, 개인 포트폴리오로 전환하여 지속 개발 중*

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

### 팀 프로젝트 (2025.05.13~06.01) — 성능·유지보수 최적화

| 지표 | 결과 |
|------|------|
| 총 테스트 케이스 수 | **58개** (Chrome·Firefox · 교차 실행 미적용) |
| 테스트 실행 시간 단축률 | **48.1%** (약 1.93배 성능 개선) |
| 전체 테스트 실행 시간 | 약 46분 → **23분** |
| 로그인 횟수 절감 | 57회 → 23회 (**34회 감소**) |
| setup 시간 절감 | 628초 → 253초 (**374초, 약 6분 14초 단축**) |
| POM 도입 후 유지보수 효율 | 수정 파일 수 최대 **96.6% 절감** |

### 개인 프로젝트 (지속 개발) — 커버리지 확장 · 크로스 브라우저 도입

| 지표 | 결과 |
|------|------|
| 총 테스트 케이스 수 (현재) | **120개** (Edge·Chrome 교차 실행 / 고유 케이스 약 67개) |
| 크로스 브라우저 매트릭스 | **Edge · Chrome 병렬 교차 실행** (`fail-fast: false` — 팀 시절 대비 신규 도입) |
| 최근 CI 테스트 통과율 | **104 / 120 (약 86.7%)** — 실패 0 · 스킵 16 (+ xfail 4 미수집) |
| CI 실행 시간 | 브라우저당 **약 8~11분** (Edge · Chrome 병렬 잡) |

> 지표 출처: 테스트 수는 `pytest` 수집 × 브라우저 매트릭스, 매트릭스/파이프라인은 `.github/workflows/test.yml`, 통과율·실행 시간은 GitHub Actions 실행 기록 기준.
>
> ⏭ **스킵**은 ① 서버 업데이트(도구 → '에이전트 마켓플레이스' 개편)로 **제거된 기능**(PPT·퀴즈 생성), ② 테스트 계정 **토큰 한도 소진으로 AI 생성이 완료되지 않는** 생성형 도구(행동특성·수업지도안·세부특기·심층조사 생성), ③ 서비스에서 **제거된 기능**(기관 페이지 링크), ④ **headless CI 한정** 위젯 미초기화(고객센터) 등 **환경·서비스 변경에 따른 의도적 스킵**으로, 테스트 자체 결함이 아닙니다. *(②는 토큰 한도 회복 시 스킵 해제만으로 통과 — 폼·네비게이션은 정상 검증됨)*

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

### 🌐 Edge·Chrome 크로스 브라우저 안정화 *(개인 프로젝트)*

> 팀 시절 Chrome 단일 실행 → 개인 프로젝트에서 **Edge·Chrome 병렬 매트릭스**를 도입하자 headless·동시성 이슈가 드러남. *Chrome은 통과하는데 Edge만 실패*하는 케이스를 재현·수정.

**4. headless Edge — 토큰 한도 테스트 타임아웃**
- **문제원인**: 두 원인이 겹침 — ① 저장 버튼 locator `//button[="저장"]`가 너무 광범위해 `element_to_be_clickable`이 DOM **첫 매치(숨겨진 버튼)**를 잡아 타임아웃, ② MUI 스위치의 숨은 `<input>`에 JS click이 headless Edge에서 **간헐적으로 React onChange로 전달 안 됨**
- **해결**: 저장 버튼을 `type="submit"`로 좁히고 **보이고+활성화된 버튼만 선택**, 토글은 **반영될 때까지 최대 3회 재클릭**

  ```python
  # Before — 첫 매치(숨김) 선택 → timeout / 토글 1회 클릭 + 5초 대기
  save_btn = self.wait.until(EC.element_to_be_clickable(self._SAVE_BTN))
  self.js_click(toggle); WebDriverWait(self.driver, 5).until(...)

  # After — 화면에 보이고 활성화된 버튼만 선택 / 토글은 반영될 때까지 재클릭
  for btn in driver.find_elements(*self._SAVE_BTN):
      if btn.is_displayed() and btn.is_enabled():
          return btn
  for _ in range(3):
      if self.is_toggle_checked(self.get_toggle()) == activate:
          return
      self.js_click(self.get_toggle())   # 안 바뀌면 재클릭
  ```
- **결과**: 로컬 headless 재현 기준 **약 20분(1184초, 타임아웃 누적) → 22초**로 단축, Chrome·Edge 양쪽 통과

**5. 회원가입 테스트 — 드라이버 행(hang)으로 인한 ReadTimeout**
- **문제원인**: `driver.get()`이 기본 전략(`normal`)에서 `load` 이벤트 종료까지 블록 → 회원가입 페이지의 끝나지 않는 리소스(트래커/소켓)로 **드라이버가 120초간 응답 불능** → 세션 오염(cascade)
- **해결**: `page_load_strategy="eager"`(DOMContentLoaded에서 반환) + `set_page_load_timeout(60)`(120초 ReadTimeout → 60초 TimeoutException으로 빠른 실패)
- **결과**: 120초 ReadTimeout으로 **다수 테스트가 cascade 실패**하던 것을 **signup 단독 60초 TimeoutException으로 격리**(cascade 제거 — 이후 테스트 정상 실행). 로컬 headless 재현 시 회원가입 5건 42초 통과 *(단, headless CI에서 signup 자체는 드물게 렌더러 타임아웃이 남는 잔존 플레이크)*

**6. 크로스 브라우저 매트릭스 — 공유 계정 레이스**
- **문제원인**: Edge·Chrome 병렬 잡이 마이페이지 파괴적 테스트(비밀번호 변경·탈퇴)에서 **동일 더미 계정 1개를 동시에 변경** → 한쪽 로그인이 거부되어 setup 단계 `TimeoutException`
- **해결**: 워크플로우에서 `matrix.browser` 분기로 **브라우저별 전용 더미 계정 주입** (테스트 코드·로컬 `.env` 무변경)

  ```yaml
  MYPAGE_USER_ID: ${{ matrix.browser == 'edge' && secrets.MYPAGE_USER_ID_EDGE || secrets.MYPAGE_USER_ID_CHROME }}
  ```
- **결과**: 마이페이지 간헐 setup ERROR **7~14건 → 0건**, Edge에서 마이페이지 **13개 케이스 스킵 → 정상 실행·통과**

---

## 📁 프로젝트 구조

```
focus/
├── config/                   # 브라우저·설정·로그인 헬퍼
│   ├── browser_factory.py    # Edge/Chrome 드라이버 생성
│   ├── settings.py           # URL·타임아웃·테스트 계정 설정
│   ├── login_helpers.py      # 공통 로그인/배너 처리
│   ├── selenium_imports.py   # Selenium 공통 import 모음
│   ├── jira_config.py        # Jira 연동 설정
│   └── requirements.txt      # 의존성 패키지
├── pages/                    # Page Object Model (3계층)
│   ├── base_page.py          # 1계층: 공통 동작
│   ├── tools/                # ✅ 담당: Tools lesson·ppt
│   ├── settings/             # ✅ 담당: Settings 세부 Page
│   ├── agents/  mypage/  token/
│   └── login/  logout/  signup/  chat/  performance/
├── tests/                    # 테스트 코드
│   ├── tools/                # ✅ 담당: Tools lesson·ppt
│   ├── settings/             # ✅ 담당
│   ├── agent/  mypage/  token/
│   └── login/  logout/  signup/  chat/
├── performance/              # 성능 부하 테스트 (top-level, testpaths 등록)
├── utils/
│   ├── jira_helper.py        # Jira 이슈 생성·스크린샷 첨부 (REST API v3)
│   └── random_generator.py   # 테스트 데이터 생성
├── scripts/
│   ├── ci_allure.py          # ✅ 담당: Allure 리포트 생성 스크립트
│   ├── ci_notify.py          # ✅ 담당: Discord 알림 스크립트
│   └── recreate_test_account.py  # 테스트 계정 재생성 CLI
├── .github/workflows/
│   └── test.yml              # ✅ 담당: GitHub Actions CI/CD (Test→Deploy→Notify)
├── conftest.py               # 공통 fixture + 실패 시 Jira 자동 등록 훅
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
# 테스트 계정 (TEST_USER_*, MYPAGE_USER_*, NON_ADMIN_USER_*) — .env.example 참고, 로그인 테스트에 필수
TEST_USER_ID=your_email@example.com
TEST_USER_PW=your_password

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
| `TEST_USER_ID` / `TEST_USER_PW` | 메인 테스트 계정 (로그인 필수 — 미설정 시 `do_login`에서 `ValueError`) |
| `MYPAGE_USER_ID` / `MYPAGE_USER_PW` / `MYPAGE_USER_NAME` | 마이페이지 전용 더미 계정 (탈퇴/재가입·비밀번호 변경 테스트용, 메인 계정과 분리 필수) |
| `MYPAGE_NEW_PASSWORD` | 비밀번호 변경 테스트에서 사용 후 원복하는 임시 비밀번호 |
| `NON_ADMIN_USER_ID` / `NON_ADMIN_USER_PW` | 비관리자 계정 (조직 설정 권한 테스트용) |
| `JIRA_URL` | Jira 인스턴스 URL |
| `JIRA_EMAIL` | Jira 계정 이메일 |
| `JIRA_API_TOKEN` | Jira API 토큰 |
| `JIRA_PROJECT_KEY` | Jira 프로젝트 키 |
| `DISCORD_WEBHOOK_URL` | Discord 웹훅 URL |

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
