"""CI용 Discord 알림 스크립트.

allure-report/widgets/summary.json 을 파싱해서 결과 요약을 Discord 웹훅으로 전송.
GitLab CI 환경 변수(CI_PROJECT_NAME, CI_PAGES_URL 등)를 자동으로 사용.

필요 GitLab CI/CD 변수:
  DISCORD_WEBHOOK_URL — Discord 웹훅 URL (Settings → CI/CD → Variables)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
if not WEBHOOK_URL:
    print("오류: DISCORD_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.", file=sys.stderr)
    print("GitLab 프로젝트 → Settings → CI/CD → Variables 에서 등록하세요.", file=sys.stderr)
    sys.exit(1)


def parse_allure_summary() -> dict:
    summary_path = Path("allure-report/widgets/summary.json")
    if not summary_path.exists():
        print("[경고] summary.json 없음 — 통계 0으로 처리")
        return {}
    try:
        with open(summary_path, encoding="utf-8") as f:
            return json.load(f).get("statistic", {})
    except Exception as e:
        print(f"[경고] summary.json 파싱 실패: {e}", file=sys.stderr)
        return {}


def build_message(stats: dict) -> str:
    passed  = stats.get("passed", 0)
    failed  = stats.get("failed", 0)
    broken  = stats.get("broken", 0)
    skipped = stats.get("skipped", 0)
    total   = stats.get("total", 0)

    project      = os.environ.get("CI_PROJECT_NAME", "프로젝트")
    branch       = os.environ.get("CI_COMMIT_BRANCH", "")
    user         = os.environ.get("GITLAB_USER_NAME", "")
    commit_title = os.environ.get("CI_COMMIT_TITLE", "")
    pages_url    = os.environ.get("CI_PAGES_URL", "")
    pipeline_url = os.environ.get("CI_PIPELINE_URL", "")

    icon = "✅" if (failed + broken) == 0 else "❌"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"{icon} **{project}** — `{branch}` 테스트 완료",
        f"📅 {date}  |  👤 {user}",
        f"💬 {commit_title}",
        "",
        f"✅ 성공: **{passed}**  ❌ 실패: **{failed + broken}**  ⏭ 스킵: **{skipped}**  합계: **{total}**",
    ]

    if pages_url:
        lines.append(f"\n📊 Allure 리포트: {pages_url}")
    if pipeline_url:
        lines.append(f"🔗 파이프라인: {pipeline_url}")

    return "\n".join(lines)


def send(message: str) -> None:
    resp = requests.post(WEBHOOK_URL, json={"content": message}, timeout=10)
    resp.raise_for_status()
    print("Discord 알림 전송 완료")


if __name__ == "__main__":
    stats = parse_allure_summary()
    message = build_message(stats)
    try:
        send(message)
    except Exception as e:
        print(f"Discord 전송 실패: {e}", file=sys.stderr)
        sys.exit(1)
