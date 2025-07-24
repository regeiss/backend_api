from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# API URLs v1
api_v1_patterns = [
    # JWT Authentication (endpoints padrão)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Custom Authentication (endpoints customizados)
    path('auth/', include('authentication.urls')),

    # Apps
    path('', include('apps.api.urls')),
    path('cadastro/', include('apps.cadastro.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1 - TODAS as rotas da API devem usar este prefixo
    path('api/v1/', include(api_v1_patterns)),

    # API Documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Home
    #path('', home_view, name='home'),
    path('', lambda request: HttpResponse("API Cadastro Unificado - v1.0.0"), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
