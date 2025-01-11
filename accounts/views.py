from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as EmailValidationError
from django.http import JsonResponse
from .tmdb import search_movies
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    user_data = [{"username": user.username, "email": user.email} for user in users]
    return Response({"users": user_data}, status=200)


@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "El nombre de usuario ya está en uso. Por favor, elige otro."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "El correo electrónico ya está registrado. Por favor, usa otro."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_email(email)
    except EmailValidationError:
        return Response(
            {"error": "El formato del correo electrónico no es válido."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(password)
    except ValidationError as e:
        return Response(
            {"error": " ".join(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"message": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_movies(request):
    user = request.user
    return Response({"message": f"Bienvenido {user.username}. Aquí están tus películas."})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies_view(request):
    query = request.query_params.get('query', '')
    if not query:
        return JsonResponse({"error": "Debes proporcionar un término."}, status=400)

    results = search_movies(query)
    return JsonResponse({"results": results}, status=200)



