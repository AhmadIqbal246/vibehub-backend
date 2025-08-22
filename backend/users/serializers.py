from rest_framework import serializers
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User



class AuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_number']

        
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture', 'profile_picture_url', 'bio', 'date_of_birth', 'gender', 'gender_display']

    def get_profile_picture_url(self, obj):
        return obj.profile_picture.url if obj.profile_picture else None


class ManualSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.get('username')

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already taken.")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # 💡 Phone number will be created in the signal

        return user
