from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, PasswordResetRequestView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView, UsersListView, UsersDisableView

app_name = UsersConfig.name

urlpatterns = [
    # регистрация и вход
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),

    # восстановление пароля
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Список пользователей сервиса
    path('users/', UsersListView.as_view(), name='users-list'),

    # блокировка пользователя сервиса
    path('users/<int:pk>/disable/', UsersDisableView.as_view(), name='users-disable'),

]

