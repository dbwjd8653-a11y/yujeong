# common/pages.py
# 프로젝트 내 모든 Page 클래스 단일 임포트 지점

from pages.base_page import BasePage
from pages.login.login_page import LoginPage
from pages.logout.logout_page import LogoutPage
from pages.signup.signup_page import SignupPage
from pages.chat.chat_page import ChatPage
from pages.token.token_page import TokenPage
from pages.tools.base_tool_page import BaseToolPage
from pages.tools.tools_specialty_page import SpecialtyPage
from pages.tools.tools_behavior_page import BehaviorPage
from pages.tools.tools_quiz_page import QuizPage
from pages.tools.tools_deep_page import DeepPage
from pages.tools.tools_lesson_page import LessonPlanPage
from pages.tools.tools_ppt_page import PPTPage
from pages.agents.agents_page import AgentsPage
from pages.agents.agents_detail_page import AgentDetailPage
from pages.mypage.mypage_page import MyPage as MyPageBase
from pages.mypage.mypage_profile_page import MyPageProfilePage
from pages.mypage.mypage_account_page import MyPage05
from pages.mypage.mypage_withdraw_page import MyPage06
from pages.mypage.mypage_organization_page import MyPage07
from pages.mypage.mypage_language_page import MyPage08
from pages.mypage.mypage_support_page import MyPage09

__all__ = [
    "BasePage",
    "LoginPage",
    "LogoutPage",
    "SignupPage",
    "ChatPage",
    "TokenPage",
    "BaseToolPage",
    "SpecialtyPage",
    "BehaviorPage",
    "QuizPage",
    "DeepPage",
    "LessonPlanPage",
    "PPTPage",
    "AgentsPage",
    "AgentDetailPage",
    "MyPageBase",
    "MyPageProfile",
    "MyPage05",
    "MyPage06",
    "MyPage07",
    "MyPage08",
    "MyPage09",
]
