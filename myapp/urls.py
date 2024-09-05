from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaViewSet, SendSMSAPIView

router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet)

urlpatterns = [
    path('send-sms/', SendSMSAPIView.as_view(), name='send-sms'),
    path('', include(router.urls)),  # Inclui as rotas do ViewSet
]
