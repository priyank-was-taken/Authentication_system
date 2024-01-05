from rest_framework import serializers
from . import models
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'password', 'password1']

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create(email=validated_data['email'], password=validated_data['password'])
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class UserLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(self.user).data
        return {'access': data['access'], 'refresh': data['refresh'], 'user': data['user']}


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=40)

    class Meta:
        model = models.User
        fields = ['email']

    def validate(self, attrs):
        user = models.User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError({"error": "email does not exist"})
        return attrs


class ForgotPasswordOtpVerificationSerializer(serializers.ModelSerializer):
    secret_key = serializers.CharField(max_length=255, )
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ['otp', 'secret_key', 'password', 'password1']

    def validate(self, attrs):
        decoded_data = jwt.decode(jwt=attrs['secret_key'],
                                  key='secret',
                                  algorithms=["HS256"])
        email = decoded_data['email']
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"error": "password doesn't match"})
        if not models.User.objects.filter(email=decoded_data['email'], otp=attrs['otp']).exists():
            raise serializers.ValidationError({"error": "user does not exist"})
        attrs['email'] = email
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = models.User
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):

        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"error": "password doesn't match"})
        return attrs
