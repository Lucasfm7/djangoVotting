from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaViewSet

# Cria o roteador para as URLs
router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas geradas pelo ViewSet
]
