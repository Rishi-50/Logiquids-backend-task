from rest_framework import serializers
from .models import User

# User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "name", "mobile_number", "city", "password"]
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(**validated_data)
        return user

# User Login Serializer
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            return user
        raise serializers.ValidationError("Invalid credentials")

# Referral Serializer
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'date_joined']
