from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics,status, views
from .models import User
from rest_framework.response import Response
from .serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from django.conf import settings
from django.urls import reverse
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes=[]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        

        abs_url = 'http://'+current_site+relative_link+"?token="+str(token)
        email_body = 'Hey there '+ user.username+ ' Use the link below to activate your account \n'+ abs_url
        data={'email_body' : email_body, 'email_subject': 'Verify your email', 'to_email' : user.email}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', 
            in_=openapi.IN_QUERY, 
            description='Description', 
            type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user=User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            
            return Response({'email' : 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error' : 'activation link expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as identifier:
            return Response({'error' : 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    permission_classes=[]
    serializer_class=LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestPasswordResetEmail(generics.CreateAPIView):
    permission_classes=[]
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token' : token})
        

            abs_url = 'http://'+current_site+relative_link
            email_body = 'Hey there Use the link below to reset your password \n'+ abs_url
            data={'email_body' : email_body, 'email_subject': 'Reset your password', 'to_email' : user.email}
            Util.send_email(data)
        return Response({'success' : 'we sent you a link, please verify your email'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes=[]
    serializer_class = ResetPasswordEmailRequestSerializer 
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error' : 'Token not valid'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success':True,'message' : 'credentials valid', 'uidb64' : uidb64, 'token' : token, 'status' : status.HTTP_200_OK})
            
        except:
            return Response({'error' : 'Token is invalid'}, status=status.status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success' : True, 'message' : 'password reset success'}, status=status.HTTP_200_OK)