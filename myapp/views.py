from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pessoa
from .serializers import PessoaSerializer

class PessoaViewSet(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer
    permission_classes = [IsAuthenticated]  # Exige autenticação

    # Método customizado para buscar Pessoa por CPF
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def pesquisar_cpf(self, request):
        cpf = request.query_params.get('cpf', None)
        if cpf:
            pessoa = Pessoa.objects.filter(cpf=cpf).first()
            if pessoa:
                serializer = PessoaSerializer(pessoa)
                return Response(serializer.data)
            return Response({"detail": "Pessoa não encontrada."}, status=404)
        return Response({"detail": "CPF não fornecido."}, status=400)
