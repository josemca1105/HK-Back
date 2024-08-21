from django.urls import path
from .views import RegisterView, LoginView, AuthView, LogoutView, UsersView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user', AuthView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('users', UsersView.as_view(), name='users_api'),
    path('users-create', UsersView.as_view(), name='users_create_api'),
]