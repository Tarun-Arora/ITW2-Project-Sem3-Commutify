from datetime import timedelta
from random import randint
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import ForgotPwdRequest, UserInfo


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300)
    password = serializers.CharField(max_length=300)

    def validate(self, data):
        user = authenticate(**data)
        # user = authenticate(username=data['username'],password=data['password'])
        if user and user.is_authenticated:
            return user
        raise serializers.ValidationError("Incorrect.")

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=300)
    last_name = serializers.CharField(max_length=300)
    dob = serializers.DateField()
    email = serializers.EmailField()

    def clean(self):
        email = self.validated_data.get('email')
        if UserInfo.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["An account with this email is already created. Try logging in."]})
        password = self.validated_data.get('password')
        if len(password) < 6:
            raise  serializers.ValidationError({"password": ["Password too weak, try different password"]})
        self.validated_data['verify_pin']=randint(100000,999999)
        return self.validated_data

    class Meta:
        model = UserInfo
        fields = ['username', 'first_name','last_name', 'email', 'password','dob']

class ResetPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    newpasswd = serializers.CharField(max_length=300,style={'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        model = ForgotPwdRequest
        fields = ['email', 'otp','newpasswd']

    def validate(self,data):
        try:
            pwd = ForgotPwdRequest.objects.get(email=data['email'],otp=data['otp'])
            if(pwd.sttime+timedelta(minutes=15)<timezone.now()):
                raise serializers.ValidationError('OTP Expired')
            data['pwd']=pwd
            return data
        except Exception as e:
            print(e)
            raise serializers.ValidationError('Invalid Info')
    
    def save(self):
        data = self.validated_data
        user = UserInfo.objects.get(email=data['email'])
        user.set_password(data['newpasswd'])
        user.save()
        data['pwd'].delete()
        return {}
