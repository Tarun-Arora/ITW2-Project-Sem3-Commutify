from random import randint

from django.conf import settings
from django.contrib.auth import login
from django.core import mail
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authentication.models import ForgotPwdRequest, UserInfo
from authentication.serializers import LoginSerializer, RegisterSerializer, ResetPasswordSerializer


def create_auth_token(user):
    """ Returns the token required for authentication for a user. """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        profile_obj = user
        if not profile_obj.is_verified:
            subject = 'Verify Commutify Account'
            message = f'Hi click the link to verify your commutify account http://commutify-server.herokuapp.com/auth/verify/{user.username}/{user.verify_pin}/'
            send_mail(user.email, subject, message)
            return Response({'msg': 'Email is not verified, check your mail.'}, status=401)
        dic = {'token': str(create_auth_token(user))}
        login(request, user)
        return Response(dic, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.clean()
        user = serializer.save()
        user.set_password(user.password)
        user.save()
        token = create_auth_token(user)
        subject = 'Verify Commutify Account'
        message = f'Hi click the link to verify your commutify account http://commutify-server.herokuapp.com/auth/verify/{user.username}/{user.verify_pin}/'
        send_mail(user.email,subject,message)
        return Response({'Success': 'You are now registered. Please verify your email.'}, status=status.HTTP_200_OK)


def send_mail(email, sub, msg):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        email = mail.EmailMessage(sub, msg, to=recipient_list)
        email.send()
    except Exception as e:
        print(e)


@csrf_exempt
@api_view(('POST',))
def forgotPwdOtp(request, email):
    try:
        user = UserInfo.objects.get(email=email)
        token = create_auth_token(user=user)
        subject = 'Commutify - Reset Password'
        otp = randint(100000, 999999)
        message = f'User {user.username},\n\tYour OTP for changing the password of your Commutify Account is {otp}.\nThis OTP is valid for 15 minutes.\nDo not share this OTP with Anyone.\nIf you didn\'t request for changing your password, just ignore this email.\n\nTeam Commutify'
        send_mail(email, subject, message)
        obj, created = ForgotPwdRequest.objects.update_or_create(
            email=email,
            defaults={'email': email, 'otp': otp}, )
        return Response({'Success': 'OTP has been sent to this email.'})
    except Exception as e:
        return Response(status=400)


class ResetPwd(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Password reset successful.'})


@csrf_exempt
@api_view(('GET',))
def verify(request, email, verify_pin):
    try:
        user = UserInfo.objects.get(email=email, verify_pin=verify_pin)
        if user:
            if user.is_verified:
                return Response({'info': 'Your account is already verified.'})
            user.is_verified = True
            user.save()
            return Response({'verified': 'Your account has been verified.'})
        else:
            return Response({'info': 'Bad Request'}, status=400)
    except Exception as e:
        return Response({'info': 'Bad Request'}, status=400)



