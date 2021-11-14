from django.urls import path

from .views import LoginView, RegisterView, verify, forgotPwdOtp, ResetPwd

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('verify/<email>/<verify_pin>/', verify, name="verify"),
    path('forgotpwd/<email>/', forgotPwdOtp, name="sendotp"),
    path('resetpwd/', ResetPwd.as_view(), name="sendotp"),
]
