from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.db import transaction
from .models import VolunteerProfile, Project, ProjectApplication, Contact


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        validators=[validate_password]
    )
    role = serializers.ChoiceField(
        choices=VolunteerProfile.ROLE_CHOICES,
        default="volunteer"
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Уже существует пользователь с таким username!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Уже существует пользователь с таким email!")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            VolunteerProfile.objects.create(
                user=user,
                role=validated_data['role']
            )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'address',
            'start_date', 'end_date', 'hours_count', 'volunteers_needed',
            'status', 'category', 'category_name', 'applications_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_applications_count(self, obj):
        return obj.applications.count()


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    coordinator_username = serializers.CharField(source='coordinator.user.username', read_only=True)
    applications_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'address',
            'start_date', 'end_date', 'hours_count', 'volunteers_needed',
            'status', 'category', 'category_name', 'coordinator', 'coordinator_username',
            'applications_count', 'created_at'
        ]
        read_only_fields = ['id', 'coordinator', 'coordinator_username', 'created_at']
        extra_kwargs = {
            'category': {'required': False, 'allow_null': True},
        }

    def get_applications_count(self, obj):
        return obj.applications.count()


class ProjectApplicationSerializer(serializers.ModelSerializer):
    volunteer_username = serializers.CharField(source='volunteer.user.username', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = ProjectApplication
        fields = [
            'id', 'project', 'project_title', 'cover_letter',
            'status', 'volunteer', 'volunteer_username', 'applied_at'
        ]
        read_only_fields = [
            'id', 'status', 'volunteer', 'volunteer_username',
            'applied_at', 'project', 'project_title'
        ]

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'topic', 'message']
        read_only_fields = ['id']
