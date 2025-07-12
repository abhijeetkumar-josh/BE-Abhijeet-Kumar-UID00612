from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id','first_name','last_name','email']

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password','id']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  
        user.save()
        Token.objects.create(user=user) 
        return user
    