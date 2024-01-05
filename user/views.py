from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from . import models
from . import serializers
from django.http.response import JsonResponse
from rest_framework_simplejwt.views import TokenViewBase
from . import email
import jwt
from rest_framework.exceptions import MethodNotAllowed


# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = ()
    serializer_class = serializers.UserRegisterSerializer


class LoginView(TokenViewBase):
    serializer_class = serializers.UserLoginSerializer


class ForgotPasswordView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = ()
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = models.User.objects.filter(email=serializer.validated_data['email']).first()
            user.otp = email.send_otp_via_email(email=serializer.validated_data['email'])
            user.save()
            secret_key = jwt.encode(payload={"email": user.email},
                                    key='secret',
                                    algorithm="HS256")

            return Response({'otp': user.otp, 'Secret_Key': secret_key},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")


class ForgotPasswordOtpVerificationView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    permission_classes = ()
    serializer_class = serializers.ForgotPasswordOtpVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['password']
            user = models.User.objects.get(email=email)
            user.set_password(new_password)
            user.otp = None
            user.save()

            return Response({'response': "successfully updated password"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")


class ResetPasswordView(generics.GenericAPIView):
    queryset = models.User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not user.check_password(old_password):
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
        return Response({'response': "successfully updated password"}, status=status.HTTP_200_OK)


def home(request):
    return JsonResponse({'message': 'Hello World!'})
