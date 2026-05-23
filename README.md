## pytest 평소 실행 (slow 제외 test)
> pytest

## slow marker까지 실행
> pytest -m "" 

## slow marker만 실행
> pytest -m slow 


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


## Discord 알림 사용
> pytest --discord tests/폴더명/


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
> pytest tests/폴더명/ --open

### 빠른 확인 (결과만 저장, 브라우저 안 열림)
> pytest tests/폴더명/

### 리포트 브라우저로 보기
> pytest tests/폴더명/ --open

### Discord로 전송 (리포트 스크린샷 포함)
> pytest tests/폴더명/ --discord


## Allure 리포트 확인 없이 테스트만 실행
> pytest tests/ --no-header -p no:allure