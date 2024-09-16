from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pessoa
from .serializers import PessoaSerializer

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

