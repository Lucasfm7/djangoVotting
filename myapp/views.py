# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client
import os

class SendSMSAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Pegue os parâmetros do corpo da requisição
        to_phone_number = request.data.get('to_phone_number')
        message_body = request.data.get('message_body')

        # Verifique se os parâmetros estão presentes
        if not to_phone_number or not message_body:
            return Response(
                {"error": "Os campos 'to_phone_number' e 'message_body' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Credenciais do Twilio
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = '81d5b540dbfac3809f055e5c0d24451b'
        twilio_phone_number = '+19389466113'

        # Crie uma instância do cliente Twilio
        client = Client(twilio_account_sid, auth_token)

        try:
            # Enviar o SMS
            message = client.messages.create(
                body=message_body,
                from_=twilio_phone_number,
                to=to_phone_number
            )
            # Retornar uma resposta de sucesso
            return Response(
                {"message": "Mensagem enviada com sucesso", "sid": message.sid},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pessoa
from .serializers import PessoaSerializer

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    # Método customizado para buscar Pessoa por CPF
    @action(detail=False, methods=['get'])
    def pesquisar_cpf(self, request):
        cpf = request.query_params.get('cpf', None)
        if cpf:
            pessoa = Pessoa.objects.filter(cpf=cpf).first()
            if pessoa:
                serializer = PessoaSerializer(pessoa)
                return Response(serializer.data)
            return Response({"detail": "Pessoa não encontrada."}, status=404)
        return Response({"detail": "CPF não fornecido."}, status=400)
