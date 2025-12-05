from .views import (
    UserAPIView, UserLogoutAPIView, UserLoginAPIView, UserRegisterationAPIView,
    AdminLoginAPIView, AdminUserListAPIView, ApproveUserAPIView, 
    PendingUsersAPIView, ApprovedUsersAPIView, UserDetailAPIView, DisapproveUserAPIView
)
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterationAPIView.as_view(), name="create-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("user/", UserAPIView.as_view(), name="user-info"),
    # Routes Admin
    path("auth/admin/login/", AdminLoginAPIView.as_view(), name="admin-login"),
    path("auth/admin/users/", AdminUserListAPIView.as_view(), name="admin-users-list"),
    path("auth/admin/users/pending/", PendingUsersAPIView.as_view(), name="admin-pending-users"),
    path("auth/admin/users/approved/", ApprovedUsersAPIView.as_view(), name="admin-approved-users"),
    path("auth/admin/users/<int:user_id>/", UserDetailAPIView.as_view(), name="admin-user-detail"),
    path("auth/admin/users/<int:user_id>/approve/", ApproveUserAPIView.as_view(), name="admin-approve-user"),
    path("auth/admin/users/<int:user_id>/disapprove/", DisapproveUserAPIView.as_view(), name="admin-disapprove-user"),

]


