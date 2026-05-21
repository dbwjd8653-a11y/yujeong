# utils/jira_helper.py

import logging

import requests
from requests.auth import HTTPBasicAuth

from config.jira_config import (
    JIRA_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    JIRA_PROJECT_KEY,
    DEFAULT_API_TIMEOUT
)

# ── Logger 설정 ───────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Jira Bug 생성 ────────────────────────────────────────────────

def create_jira_bug_ticket(summary, description):

    url = f"{JIRA_URL}/rest/api/2/issue"

    auth = HTTPBasicAuth(
        JIRA_EMAIL,
        JIRA_API_TOKEN
    )

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": "버그"
            },
            "labels": [
                "Automation",
                "UI-Test"
            ]
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            auth=auth,
            timeout=DEFAULT_API_TIMEOUT
        )

        if response.status_code == 201:

            issue_key = response.json().get("key")

            logger.info(
                f"Jira 티켓 생성 성공: "
                f"{JIRA_URL}/browse/{issue_key}"
            )

            return issue_key

        else:

            logger.error(
                f"Jira 생성 실패: "
                f"{response.status_code}, "
                f"{response.text}"
            )

            return None

    except Exception as e:

        logger.error(f"Jira 통신 오류: {e}")

        return None

# ── Jira 스크린샷 첨부 ────────────────────────────────────────────

def attach_image_to_jira(issue_key, image_bytes):

    url = (
        f"{JIRA_URL}/rest/api/2/issue/"
        f"{issue_key}/attachments"
    )

    auth = HTTPBasicAuth(
        JIRA_EMAIL,
        JIRA_API_TOKEN
    )

    headers = {
        "X-Atlassian-Token": "no-check"
    }

    files = {
        "file": (
            "error_screenshot.png",
            image_bytes,
            "image/png"
        )
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            files=files,
            timeout=DEFAULT_API_TIMEOUT + 10
        )

        if response.status_code == 200:

            logger.info(
                "스크린샷 첨부 성공"
            )

        else:

            logger.error(
                f"스크린샷 첨부 실패: "
                f"{response.status_code}, "
                f"{response.text}"
            )

    except Exception as e:

        logger.error(
            f"스크린샷 첨부 오류: {e}"
        )