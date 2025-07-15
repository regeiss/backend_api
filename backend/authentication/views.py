# backend/authentication/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import serializers


# Serializers para as views de autenticação
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    token = serializers.CharField(required=False)
    refresh = serializers.CharField(required=False)
    message = serializers.CharField(required=False)
    user = serializers.JSONField(required=False)


class UserProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_staff = serializers.BooleanField()
    is_active = serializers.BooleanField()
    date_joined = serializers.CharField()


class LogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False)


class LogoutResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()


class ChangePasswordRequestSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()


class ChangePasswordResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()


@extend_schema(
    summary="Login de usuário",
    description="Autentica um usuário e retorna tokens JWT",
    request=LoginRequestSerializer,
    responses={200: LoginResponseSerializer}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': 'Username e password são obrigatórios'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        if user.is_active:
            # Gerar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'success': True,
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.isoformat(),
                }
            })
        else:
            return Response({
                'success': False,
                'message': 'Conta desativada'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'success': False,
            'message': 'Credenciais inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    summary="Perfil do usuário",
    description="Retorna informações do usuário logado",
    responses={200: UserProfileSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'date_joined': user.date_joined.isoformat(),
    })


@extend_schema(
    summary="Logout de usuário",
    description="Faz logout do usuário e adiciona refresh token na blacklist",
    request=LogoutRequestSerializer,
    responses={200: LogoutResponseSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Erro ao fazer logout'
        }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Alterar senha",
    description="Altera a senha do usuário logado",
    request=ChangePasswordRequestSerializer,
    responses={200: ChangePasswordResponseSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(current_password):
        return Response({
            'success': False,
            'message': 'Senha atual incorreta'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({
        'success': True,
        'message': 'Senha alterada com sucesso'
    })