from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .serializers import (
    RegisterSerializer, LoginSerializer,
    ProjectSerializer, ProjectApplicationSerializer, ContactSerializer
)
from .models import Project, VolunteerProfile, Contact


# ── FBVs ────────────────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'role': user.volunteer_profile.role,
            'message': 'Регистрация успешно прошла!',
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'role': user.volunteer_profile.role,
            'message': 'Вы успешно вошли!'
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'message': 'Вы вышли из системы'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Неверный токен'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'Жоба табылмады'}, status=status.HTTP_404_NOT_FOUND)

    try:
        volunteer = request.user.volunteer_profile
    except VolunteerProfile.DoesNotExist:
        return Response({'error': 'Волонтер профилі табылмады'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProjectApplicationSerializer(
        data={'cover_letter': request.data.get('cover_letter', '')}
    )
    if serializer.is_valid():
        try:
            serializer.save(volunteer=volunteer, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'error': 'Сіз бұл жобаға өтінім бергенсіз'},
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def ratings_view(request):
    profiles = VolunteerProfile.objects.filter(is_active=True).order_by('-totalHour')[:10]
    data = [
        {
            'rank': i + 1,
            'username': p.user.username,
            'totalHour': p.totalHour,
            'initials': p.user.username[:2].upper(),
        }
        for i, p in enumerate(profiles)
    ]
    return Response(data)


# ── CBVs ────────────────────────────────────────────────────────────────────

class ProjectListCreateView(APIView):
    def get(self, request):
        projects = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Аутентификация қажет'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response({'error': 'Жоба табылмады'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProjectSerializer(project).data)

    def put(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response({'error': 'Жоба табылмады'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response({'error': 'Жоба табылмады'}, status=status.HTTP_404_NOT_FOUND)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactAPIView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

