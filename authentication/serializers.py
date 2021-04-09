from authentication.utils import Util
from rest_framework import generics, serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes, force_str, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length =68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError(
                'username should only contail alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=255, min_length=3, read_only=True)
    
    class Meta:
        model=User
        fields=['email', 'password', 'username','tokens']

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        filtered_user_by_email = User.objects.all().filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again!!')
        
        if filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue login using '+ filtered_user_by_email[0].auth_provider
            )

        if not user.is_active:
            raise AuthenticationFailed('Account is not active')

        if not user.is_verified:
            raise AuthenticationFailed('email not verified')
        
        
        return {
            'email':user.email,
            'username':user.username,
            'tokens':user.tokens
        }

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = '__all__'


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(min_length=1)
    uidb64 = serializers.CharField(min_length=1)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The link is invalid')
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The link is invalid')
        return super().validate(attrs)

    