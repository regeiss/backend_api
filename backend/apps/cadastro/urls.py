from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlojamentoViewSet, CepAtingidoViewSet, DemandaAmbienteViewSet,
    DemandaEducacaoViewSet, DemandaHabitacaoViewSet, DemandaInternaViewSet,
    DemandaSaudeViewSet, DesaparecidoViewSet, MembroViewSet, ResponsavelViewSet
)

# Configuração do router para as APIs
router = DefaultRouter()
router.register(r'alojamentos', AlojamentoViewSet)
router.register(r'ceps-atingidos', CepAtingidoViewSet)
router.register(r'responsaveis', ResponsavelViewSet)
router.register(r'membros', MembroViewSet)
router.register(r'demandas-ambiente', DemandaAmbienteViewSet)
router.register(r'demandas-educacao', DemandaEducacaoViewSet)
router.register(r'demandas-habitacao', DemandaHabitacaoViewSet)
router.register(r'demandas-internas', DemandaInternaViewSet)
router.register(r'demandas-saude', DemandaSaudeViewSet)
router.register(r'desaparecidos', DesaparecidoViewSet)

app_name = 'cadastro'

urlpatterns = [
    # API routes
    path('api/', include(router.urls)),

    # URLs específicas para ações customizadas podem ser adicionadas aqui
    # path('api/custom-endpoint/', custom_view, name='custom-endpoint'),
]

# URLs da API com prefixo de versão (opcional)
api_v1_patterns = [
    path('v1/', include(router.urls)),
]
