# common/pages.py
# 프로젝트 내 모든 Page 클래스 단일 임포트 지점

from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.signup_page import SignupPage
from pages.chat_page import ChatPage
from pages.token_page import TokenPage
from pages.tools.base_tool_page import BaseToolPage
<<<<<<< Updated upstream
from pages.tools.tools_01_page import SpecialtyPage
from pages.tools.tools_02_page import BehaviorPage
from pages.tools.tools_05_page import Tool5Page
from pages.tools.tools_06_page import Tool6Page
=======
from pages.tools.tools_specialty_page import SpecialtyPage
from pages.tools.tools_behavior_page import BehaviorPage
from pages.tools.tools_05_quiz import Tool5Page
from pages.tools.tools_06_deep import Tool6Page
>>>>>>> Stashed changes
from pages.tools.lesson_plan_page import LessonPlanPage
from pages.tools.ppt_page import PPTPage
from pages.agents.agents_page import AgentsPage
from pages.agents.agents_detail_page import AgentDetailPage
from pages.mypage.mypage_page import MyPage as MyPageBase
from pages.mypage.mypage_profile_page import MyPage as MyPageProfile
from pages.mypage.mypage_05_page import MyPage05
from pages.mypage.mypage_06_page import MyPage06
from pages.mypage.mypage_07_page import MyPage07
from pages.mypage.mypage_08_page import MyPage08
from pages.mypage.mypage_09_page import MyPage09

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
    "Tool5Page",
    "Tool6Page",
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
