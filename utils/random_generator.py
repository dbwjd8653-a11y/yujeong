# utils/random_generator.py

# ── 랜덤 테스트 이메일 생성 ───────────────────────────────────────

from datetime import datetime


def generate_test_email(prefix="autotest"):
    """
    [test_signup.py] 테스트용 랜덤 이메일 생성 함수

    형식:
        autotest_20260520201530123@test.com
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )[:-3]

    return (
        f"{prefix}_{timestamp}"
        "@test.com"
    )