# utils/random_generator.py

# ── 랜덤 테스트 이메일 생성 ───────────────────────────────────────

from datetime import datetime


def generate_test_email(prefix="autotest"):
    """
    [test_signup.py] 테스트용 랜덤 이메일 생성 함수

    형식:
        autotest_20260520201530123@test.com
    """

    # 현재 시간을 문자열로 변환
    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )[:-3]

    # 이메일 조합 후 반환
    return (
        f"{prefix}_{timestamp}"
        "@test.com"
    )