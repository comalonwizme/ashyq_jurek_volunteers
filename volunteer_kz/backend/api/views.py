from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username,
                'role': user.volunteer_profile.role,
                'message': 'Регистрация успешно прошла!',
            }, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)