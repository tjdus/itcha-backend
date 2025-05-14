from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.core.views.login import LoginView, SignUpView
from apps.core.views.token import  RefreshTokenView

urlpatterns = [
    path('token/refresh', RefreshTokenView.as_view(), name='token_refresh'),
    path('auth/login', LoginView.as_view(), name='auth_login'),
    path('auth/signup', SignUpView.as_view(), name='auth_signup'),
]