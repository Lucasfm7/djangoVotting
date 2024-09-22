# myapp/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pessoa, Candidate, Vote
from .serializers import PessoaSerializer, CandidateSerializer, VoteSerializer
from twilio.rest import Client
import os

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
