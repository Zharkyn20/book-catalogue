from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView, CodeVerificationView
from .views import UserMeView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegistrationView.as_view(), name="auth_register"),
    path("auth/verify-code/", CodeVerificationView.as_view(), name="verify-code"),
    path("auth/me/", UserMeView.as_view(), name="user-me"),
]
