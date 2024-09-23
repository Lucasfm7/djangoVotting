# myapp/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pessoa, Candidate, Vote, VerificationCode
from .serializers import (
    PessoaSerializer, 
    CandidateSerializer, 
    VoteSerializer, 
    VerificationCodeSerializer
)
from twilio.rest import Client
import os
import random
import logging
from django.utils import timezone

# Configurar o logger
logger = logging.getLogger(__name__)

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    # Desabilitar a listagem de todos os registros
    def list(self, request, *args, **kwargs):
        return Response({"error": "A listagem de CPFs não é permitida."}, status=status.HTTP_403_FORBIDDEN)

    # Desabilitar criação de registros
    def create(self, request, *args, **kwargs):
        return Response({"error": "A criação de CPFs não é permitida."}, status=status.HTTP_403_FORBIDDEN)

    # Desabilitar atualização de registros
    def update(self, request, *args, **kwargs):
        return Response({"error": "A atualização de CPFs não é permitida."}, status=status.HTTP_403_FORBIDDEN)

    # Permitir apenas a pesquisa por CPF
    @action(detail=False, methods=['get'])
    def pesquisar_cpf(self, request):
        cpf = request.query_params.get('cpf', None)
        if not cpf:
            return Response({"detail": "CPF não fornecido."}, status=status.HTTP_400_BAD_REQUEST)

        pessoa = Pessoa.objects.filter(cpf=cpf).first()
        if pessoa:
            serializer = PessoaSerializer(pessoa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "CPF não encontrado."}, status=status.HTTP_404_NOT_FOUND)

class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar candidatos.
    Não permite criação, atualização ou deleção via API.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

class VoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para registrar votos.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        return Response(VoteSerializer(vote).data, status=status.HTTP_201_CREATED)

class SendSMSView(APIView):
    """
    API para enviar SMS via Twilio.
    Requer 'message' e 'phone_number' no corpo da requisição.
    """
    def post(self, request, format=None):
        message = request.data.get('message')
        phone_number = request.data.get('phone_number')

        if not message or not phone_number:
            return Response({"detail": "Mensagem e número de telefone são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Configurar as credenciais do Twilio via variáveis de ambiente
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_FROM_NUMBER')

        if not all([account_sid, auth_token, from_number]):
            return Response({"detail": "Configurações do Twilio não estão completas."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )
            return Response({"detail": "SMS enviado com sucesso.", "sid": message.sid}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendVerificationCodeView(APIView):
    """
    API para gerar e enviar o código de verificação via SMS.
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({"detail": "Número de telefone é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Gerar um código de 6 dígitos
        code = f"{random.randint(0, 999999):06d}"

        # Atualizar ou criar o código de verificação para o número de telefone
        verification, created = VerificationCode.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'code': code,
                'created_at': timezone.now(),
                'is_verified': False
            }
        )

        # Enviar o SMS via Twilio
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_FROM_NUMBER')

        if not all([account_sid, auth_token, from_number]):
            logger.error("Configurações do Twilio incompletas.")
            return Response({"detail": "Configurações do Twilio não estão completas."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            client = Client(account_sid, auth_token)
            message_body = f"Seu código de verificação é: {code}"
            client.messages.create(
                body=message_body,
                from_=from_number,
                to=phone_number
            )
            logger.info(f"Código de verificação enviado para {phone_number}.")
        except Exception as e:
            logger.error(f"Erro ao enviar SMS para {phone_number}: {str(e)}")
            return Response({"detail": "Erro ao enviar SMS."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"detail": "Código de verificação enviado com sucesso."}, status=status.HTTP_200_OK)

class VerifyCodeView(APIView):
    """
    API para verificar o código de verificação enviado via SMS.
    """
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if not phone_number or not code:
            return Response({"detail": "Número de telefone e código são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            verification = VerificationCode.objects.get(phone_number=phone_number, code=code, is_verified=False)
        except VerificationCode.DoesNotExist:
            return Response({"detail": "Código inválido ou já verificado."}, status=status.HTTP_400_BAD_REQUEST)
        
        if verification.is_expired():
            return Response({"detail": "Código expirou."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Marcar o código como verificado
        verification.is_verified = True
        verification.save()

        # Aqui você pode adicionar lógica adicional, como associar o telefone a um usuário, etc.

        logger.info(f"Código de verificação para {phone_number} foi verificado com sucesso.")
        return Response({"detail": "Código verificado com sucesso."}, status=status.HTTP_200_OK)