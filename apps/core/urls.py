from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.core.views.check import EmailDuplicationCheckView, UsernameDuplicationCheckView
from apps.core.views.login import LoginView, SignUpView
from apps.core.views.member import MemberListView, MemberDetailView
from apps.core.views.token import  RefreshTokenView

urlpatterns = [
    path('token/refresh', RefreshTokenView.as_view(), name='token_refresh'),
    path('auth/login', LoginView.as_view(), name='auth_login'),
    path('auth/signup', SignUpView.as_view(), name='auth_signup'),
    path('auth/check-email', EmailDuplicationCheckView.as_view(), name='auth_check_email'),
    path('auth/check-username', UsernameDuplicationCheckView.as_view(), name='auth_check_username'),
    path('members', MemberListView.as_view(), name='members'),
    path('members/<int:pk>', MemberDetailView.as_view(), name='members_detail'),
]