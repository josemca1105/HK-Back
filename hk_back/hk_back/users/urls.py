from django.urls import path
from .views import (
    LoginView,
    AuthView,
    LogoutView,
    UsersListView,
    UserCreateView,
    UserDetailView,
    RequestPasswordResetEmail,
    PasswordTokenCheck,
    SetNewPassword
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('auth', AuthView.as_view(), name='auth'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('users', UsersListView.as_view(), name='users_api'),
    path('users-create', UserCreateView.as_view(), name='users_create_api'),
    path('users/<int:id>', UserDetailView.as_view(), name='users_detail_api'),
    path('users-update/<int:id>', UserDetailView.as_view(), name='users_update_api'),
    path('users-delete/<int:id>', UserDetailView.as_view(), name='users_delete_api'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<str:uidb64>/<str:token>', PasswordTokenCheck.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPassword.as_view(), name='password-reset-complete')
]