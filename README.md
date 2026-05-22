## Discord 알림 사용

```bash
pytest --discord tests/폴더명/
```

## Allure 리포트 환경 설정
### Allure 설치 순서
#### 사전 준비

* Scoop 없는 경우 먼저 설치

```bash
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

1. Java 설치 (Allure 실행에 필요) - scoop 사용
```bash
scoop bucket add java
scoop install temurin-lts
```

2. Python 패키지 설치
VS Code 터미널에서 우측 상단 + 옆 드롭다운 → PowerShell 선택
```bash
    pip install allure-pytest
```
3. Allure CLI 설치

```bash
scoop install allure
```

4. 설치 확인
```bash
java -version
allure --version
pip show allure-pytest
```
* Scoop 설치 시 팝업이 뜨면 Yes 또는 A(모두 허용) 선택

## Allure 리포트 확인
```bash
pytest tests/폴더명/ --open
```

### 빠른 확인 (결과만 저장, 브라우저 안 열림)
```bash
pytest tests/폴더명/
```

### 리포트 브라우저로 보기
```bash
pytest tests/폴더명/ --open
```

### Discord로 전송 (리포트 스크린샷 포함)
```bash
pytest tests/폴더명/ --discord
```