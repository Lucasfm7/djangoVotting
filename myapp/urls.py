# myapp/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PessoaViewSet, CandidateViewSet, VoteViewSet, SendSMSView

router = DefaultRouter()
router.register(r'pessoas', PessoaViewSet, basename='pessoa')
router.register(r'candidatos', CandidateViewSet, basename='candidate')
router.register(r'votos', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
    path('enviar_sms/', SendSMSView.as_view(), name='enviar_sms'),
]
