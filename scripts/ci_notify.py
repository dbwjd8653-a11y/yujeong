"""CI용 Discord 알림 스크립트.

allure-report/widgets/summary.json 을 파싱해서 결과 요약을 Discord 웹훅으로 전송.
GitLab CI 환경 변수(CI_PROJECT_NAME, CI_PAGES_URL 등)를 자동으로 사용.

필요 GitLab CI/CD 변수:
  DISCORD_WEBHOOK_URL — Discord 웹훅 URL (Settings → CI/CD → Variables)
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

KST = timezone(timedelta(hours=9))

import requests

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
if not WEBHOOK_URL:
    print("오류: DISCORD_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.", file=sys.stderr)
    print("GitLab 프로젝트 → Settings → CI/CD → Variables 에서 등록하세요.", file=sys.stderr)
    sys.exit(1)


def parse_allure_summary() -> tuple[dict, list[str]]:
    summary_path = Path("public/widgets/summary.json")
    if summary_path.exists():
        try:
            with open(summary_path, encoding="utf-8") as f:
                stats = json.load(f).get("statistic", {})
            if stats.get("total", 0) > 0:
                failed_names = _get_failed_names()
                return stats, failed_names
        except Exception as e:
            print(f"[경고] summary.json 파싱 실패: {e}", file=sys.stderr)

    print("[정보] allure-results 직접 파싱으로 전환")
    return _parse_from_results()


def _get_failed_names() -> list[str]:
    """public/data/suites.json 또는 allure-results에서 실패 TC 이름 수집"""
    suites_path = Path("public/data/suites.json")
    if suites_path.exists():
        try:
            with open(suites_path, encoding="utf-8") as f:
                data = json.load(f)
            names: list[str] = []
            _collect_failed(data, names)
            return names
        except Exception as e:
            print(f"[경고] suites.json 파싱 실패: {e}", file=sys.stderr)

    _, names = _parse_from_results()
    return names


def _collect_failed(node: dict, names: list[str]) -> None:
    """suites.json 노드를 재귀 순회하여 failed/broken 이름 수집"""
    if node.get("status") in ("failed", "broken"):
        names.append(node.get("name", "unknown"))
    for child in node.get("children", []):
        _collect_failed(child, names)


def _parse_from_results() -> tuple[dict, list[str]]:
    results_dir = Path("allure-results")
    if not results_dir.exists():
        print("[경고] allure-results 디렉터리 없음")
        return {}, []

    stats = {"passed": 0, "failed": 0, "broken": 0, "skipped": 0, "total": 0}
    failed_names: list[str] = []
    for result_file in results_dir.glob("*-result.json"):
        try:
            with open(result_file, encoding="utf-8") as f:
                data = json.load(f)
            status = data.get("status", "")
            if status in stats:
                stats[status] += 1
            stats["total"] += 1
            if status in ("failed", "broken"):
                name = data.get("name") or data.get("fullName", result_file.stem)
                failed_names.append(name)
        except Exception:
            pass

    return stats, failed_names


def parse_jira_tickets() -> list[dict]:
    """conftest가 기록한 jira_tickets_*.json을 모아 key 기준 중복 제거 후 반환.

    --jira 옵션이 꺼져 있으면 파일이 없으므로 빈 리스트를 반환한다(섹션 생략).
    """
    results_dir = Path("allure-results")
    if not results_dir.exists():
        return []

    seen: set[str] = set()
    tickets: list[dict] = []
    for f in sorted(results_dir.glob("jira_tickets*.json")):
        try:
            with open(f, encoding="utf-8") as fp:
                data = json.load(fp)
        except Exception as e:
            print(f"[경고] {f.name} 파싱 실패: {e}", file=sys.stderr)
            continue
        for t in data:
            key = t.get("key")
            if key and key not in seen:
                seen.add(key)
                tickets.append(t)
    return tickets


def build_message(stats: dict, failed_names: list[str], tickets: list[dict] | None = None) -> str:
    passed  = stats.get("passed", 0)
    failed  = stats.get("failed", 0)
    broken  = stats.get("broken", 0)
    skipped = stats.get("skipped", 0)
    total   = stats.get("total", 0)

    project      = os.environ.get("CI_PROJECT_NAME", "프로젝트")
    branch       = os.environ.get("CI_COMMIT_BRANCH", "")
    user         = os.environ.get("GITLAB_USER_NAME", "")
    commit_msg   = os.environ.get("CI_COMMIT_TITLE", "")
    commit_title = commit_msg.splitlines()[0] if commit_msg else ""
    pages_url    = os.environ.get("CI_PAGES_URL", "")
    pipeline_url = os.environ.get("CI_PIPELINE_URL", "")

    icon = "✅" if (failed + broken) == 0 else "❌"
    date = datetime.now(KST).strftime("%Y-%m-%d %H:%M KST")

    lines = [
        f"{icon} **{project}** `{branch}` — {commit_title}",
        f"📅 {date}  |  👤 {user}",
        f"✅ {passed}  ❌ {failed + broken}  ⏭ {skipped}  / {total}",
    ]

    if failed_names:
        lines.append("")
        lines.append("❌ 실패 목록:")
        for name in failed_names[:3]:
            lines.append(f"  · {name}")
        rest = len(failed_names) - 3
        if rest > 0:
            lines.append(f"  외 {rest}건")

    if tickets:
        lines.append("")
        lines.append(f"🐞 등록된 버그 ({len(tickets)}건):")
        for t in tickets[:5]:
            lines.append(f"  · [{t.get('key')}] {t.get('test')} → {t.get('url')}")
        rest = len(tickets) - 5
        if rest > 0:
            lines.append(f"  외 {rest}건")

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
    stats, failed_names = parse_allure_summary()
    tickets = parse_jira_tickets()
    message = build_message(stats, failed_names, tickets)
    try:
        send(message)
    except Exception as e:
        print(f"Discord 전송 실패: {e}", file=sys.stderr)
        sys.exit(1)
