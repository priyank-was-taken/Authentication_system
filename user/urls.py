from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='signupP'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('forgot/', views.ForgotPasswordView.as_view(), name='forgot'),
    path('otp-verification/', views.ForgotPasswordOtpVerificationView.as_view(), name='otp'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('home/', views.home, name='home')
]