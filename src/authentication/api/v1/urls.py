from django.urls import path
from .views.login import LoginView
from .views.register import RegisterView
from .views.reset_password import ResetPasswordRequestView, ResetPasswordView
from .views.user import UserView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset-password-token/', ResetPasswordRequestView.as_view(), name='reset-password-token'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
