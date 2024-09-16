from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaViewSet, PesquisarPessoaPorCPFAPIView

# Cria o roteador para as URLs
router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet)

urlpatterns = [
    # path('send-sms/', SendSMSAPIView.as_view(), name='send-sms'),
    path('pesquisar-pessoa-cpf/', PesquisarPessoaPorCPFAPIView.as_view(), name='pesquisar-pessoa-cpf'),
    path('', include(router.urls)),  # Inclui as rotas geradas pelo ViewSet
]
