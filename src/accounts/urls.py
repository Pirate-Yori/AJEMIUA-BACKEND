from .views import (
    UserAPIView, UserLogoutAPIView, UserLoginAPIView,
    AdminLoginAPIView, AdminUserListAPIView, UserDetailAPIView,
    ImportUsersFromExcelAPIView, ChangePasswordAPIView,
)
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
app_name = "accounts"

urlpatterns = [
    # Routes Utilisateur
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("user/", UserAPIView.as_view(), name="user-info"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    
    # Routes Admin
    path("auth/admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("auth/admin/users/", AdminUserListAPIView.as_view(), name="admin-users-list"),
    path("auth/admin/users/<int:id>/", UserDetailAPIView.as_view(), name="admin-user-detail"),
    path("auth/admin/users/import-excel/", ImportUsersFromExcelAPIView.as_view(), name="admin-import-users"),
]


