"""CI용 Allure 리포트 생성 및 GitLab Pages 배포 스크립트.

흐름:
  1. allure-history 캐시 → allure-results/history 복원 (트렌드 유지)
  2. allure generate
  3. allure-report/history → allure-history 캐시 저장
  4. allure-report → public/ 복사 (GitLab Pages artifact)
"""

import shutil
import subprocess
import sys
from pathlib import Path

RESULTS_DIR = Path("allure-results")
HISTORY_CACHE = Path("allure-history")
REPORT_DIR = Path("allure-report")
PUBLIC_DIR = Path("public")


def restore_history() -> None:
    cached = HISTORY_CACHE / "history"
    if not cached.exists():
        print("이전 히스토리 없음 — 첫 빌드로 진행")
        return
    dst = RESULTS_DIR / "history"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(str(cached), str(dst))
    print("히스토리 복원 완료")


def generate_report() -> bool:
    result = subprocess.run(
        f'allure generate "{RESULTS_DIR}" -o "{REPORT_DIR}" --clean',
        capture_output=True,
        text=True,
        shell=True,
    )
    if result.returncode != 0:
        print(f"[경고] allure generate 실패:\n{result.stderr}", file=sys.stderr)
        return False
    print("Allure 리포트 생성 완료")
    return True


def cache_history() -> None:
    src = REPORT_DIR / "history"
    if not src.exists():
        return
    if HISTORY_CACHE.exists():
        shutil.rmtree(HISTORY_CACHE)
    HISTORY_CACHE.mkdir(parents=True)
    shutil.copytree(str(src), str(HISTORY_CACHE / "history"))
    print("히스토리 캐시 저장 완료")


def deploy_to_pages() -> None:
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)

    if REPORT_DIR.exists():
        shutil.copytree(str(REPORT_DIR), str(PUBLIC_DIR), dirs_exist_ok=True)
        print(f"Allure 리포트 → {PUBLIC_DIR} 배포 완료")
    else:
        (PUBLIC_DIR / "index.html").write_text(
            "<h1>Allure report unavailable</h1>", encoding="utf-8"
        )
        print("[경고] allure-report 없음 — placeholder 생성")


if __name__ == "__main__":
    restore_history()
    generate_report()
    cache_history()
    deploy_to_pages()
