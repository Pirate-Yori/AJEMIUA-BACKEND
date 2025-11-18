from .views import UserAPIView,UserLogoutAPIView,UserLoginAPIView,UserRegisterationAPIView,RetrieveUpdateAPIView
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("user/", UserAPIView.as_view(), name="user-info"),

]