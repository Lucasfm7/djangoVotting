from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        if cpf:
            pessoa = Pessoa.objects.filter(cpf=cpf).first()
            if pessoa:
                serializer = PessoaSerializer(pessoa)
                return Response(serializer.data)
            return Response({"detail": "CPF não encontrado."}, status=404)
        return Response({"detail": "CPF não fornecido."}, status=400)

class PesquisarPessoaPorCPFAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtém o CPF dos parâmetros da URL
        cpf = request.query_params.get('cpf')

        if not cpf:
            return Response(
                {"error": "O campo 'cpf' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pesquisa a pessoa com o CPF fornecido
        pessoa = Pessoa.objects.filter(cpf=cpf).first()

        if pessoa:
            # Serializa a instância da Pessoa encontrada
            serializer = PessoaSerializer(pessoa)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Pessoa não encontrada."},
                status=status.HTTP_404_NOT_FOUND
            )
