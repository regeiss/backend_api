from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Login customizado",
    description="Endpoint de login com resposta customizada",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'}
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'success': {'type': 'boolean'},
                'token': {'type': 'string'},
                'refresh': {'type': 'string'},
                'user': {'type': 'object'}
            }
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login customizado com resposta no formato esperado pelo Flutter
    """
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validar campos obrigatórios
        if not username or not password:
            return Response({
                'success': False,
                'message': 'Username e password são obrigatórios',
                'error': 'MISSING_CREDENTIALS'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Autenticar usuário
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                # Gerar tokens JWT
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'success': True,
                    'message': 'Login realizado com sucesso',
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
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Conta desativada',
                    'error': 'ACCOUNT_DISABLED'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'success': False,
                'message': 'Credenciais inválidas',
                'error': 'INVALID_CREDENTIALS'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Erro interno do servidor',
            'error': 'INTERNAL_ERROR',
            'details': str(e) if settings.DEBUG else None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(summary="Perfil do usuário")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    Retorna informações do usuário logado
    """
    user = request.user
    return Response({
        'success': True,
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

@extend_schema(summary="Logout")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout com blacklist do refresh token
    """
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
            'message': 'Erro ao fazer logout',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(summary="Alterar senha")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    Altera a senha do usuário
    """
    try:
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        
        if not current_password or not new_password:
            return Response({
                'success': False,
                'message': 'Senha atual e nova senha são obrigatórias'
            }, status=status.HTTP_400_BAD_REQUEST)
        
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
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Erro ao alterar senha',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
