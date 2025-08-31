from django.urls import path
from .views import (
    RegisterView, VerifyEmailView,
    ResetPasswordRequestView, ResetPasswordConfirmView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password'),
    path('reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
]
