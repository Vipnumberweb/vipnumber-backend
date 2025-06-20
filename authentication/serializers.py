from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import VN_User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = VN_User
        fields = '__all__'
        read_only_fields = ('id',) 

    def validate(self, data):
        # Ensure at least one of username, email, or phone is provided
        if not (data.get('username') or data.get('email') or data.get('phone')):
            raise serializers.ValidationError(
                "At least one of username, email, or phone must be provided."
            )
        return data

    def create(self, validated_data):
        # Create the user with the provided data
        user = VN_User.objects.create_user(
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            username=validated_data.get('username', ''),
            email=validated_data.get('email', ''),
            phone=validated_data['phone'],
            password=validated_data['password'],
            is_vendor=validated_data.get('is_vendor', False),
        )
        # Set phone_verified to False by default if not provided
        user.phone_verified = False
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        # First try to find the user
        user = VN_User.objects.filter(
            models.Q(username=identifier) |
            models.Q(email=identifier) |
            models.Q(phone=identifier)
        ).first()

        if not user:
            raise serializers.ValidationError("No account found with this username, email, or phone number.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")

        data['user'] = user
        return data

class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

