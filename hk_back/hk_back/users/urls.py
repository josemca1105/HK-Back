from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    AuthView,
    LogoutView,
    UsersListView,
    UserCreateView,
    UserDetailView
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user', AuthView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('users', UsersListView.as_view(), name='users_api'),
    path('users-create', UserCreateView.as_view(), name='users_create_api'),
    path('users-update/<int:id>', UserDetailView.as_view(), name='users_update_api'),
    path('users-delete/<int:id>', UserDetailView.as_view(), name='users_delete_api'),
]