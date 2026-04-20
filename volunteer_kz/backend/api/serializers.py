from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import VolunteerProfile
from django.contrib.auth.models import User
from django.db import transaction

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 150)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length = 6, 
        write_only=True, 
        validators = [validate_password]
        )
    
    phone_number = serializers.CharField(max_length = 20)

    role = serializers.ChoiceField(
        choices=VolunteerProfile.ROLE_CHOICES,
        default = "volunteer"
    )

    def validate_username(self, value):
        if User.objects.filter(username = value).exists():
            raise serializers.ValidationError("Уже существует пользователь с таким username!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Уже существует пользователь с таким email!")
        return value
    
    def validate_phone_number(self, value):
        if VolunteerProfile.objects.filter(phone_number = value).exists():
            raise serializers.ValidationError("Уже существует пользователь с таким номером телефона!")
        return value
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username = validated_data['username'],
                email =  validated_data['email'],
                password = validated_data['password']
            )
            VolunteerProfile.objects.create(
                user = user,
                phone_number = validated_data["phone_number"],
                role = validated_data["role"]
            )
        return user