# myapp/serializers.py

from rest_framework import serializers
from .models import Pessoa, Candidate, Vote, VerificationCode

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = ['id', 'nome', 'cpf', 'empresa', 'segmento', 'ja_votou']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'nome']

class VoteSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)
    cpf = serializers.CharField(write_only=True)
    candidate_id = serializers.IntegerField(write_only=True)
    nome = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    sobrenome = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    telefone = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Vote
        fields = [
            'id',
            'pessoa',
            'candidate',
            'timestamp',
            'cpf',
            'candidate_id',
            'nome',
            'sobrenome',
            'telefone'
        ]
        read_only_fields = ['id', 'pessoa', 'candidate', 'timestamp']

    def create(self, validated_data):
        cpf = validated_data.pop('cpf')
        candidate_id = validated_data.pop('candidate_id')

        nome = validated_data.get('nome')
        sobrenome = validated_data.get('sobrenome')
        telefone = validated_data.get('telefone')

        try:
            pessoa = Pessoa.objects.get(cpf=cpf)
        except Pessoa.DoesNotExist:
            raise serializers.ValidationError({"cpf": "CPF não encontrado."})

        try:
            candidate = Candidate.objects.get(id=candidate_id)
        except Candidate.DoesNotExist:
            raise serializers.ValidationError({"candidate_id": "Candidato não encontrado."})

        # Verifica se a pessoa já votou
        if pessoa.ja_votou:
            raise serializers.ValidationError({"detail": "Esta pessoa já votou."})

        # Prepara os dados para criar o voto
        vote_data = {
            'pessoa': pessoa,
            'candidate': candidate,
            'nome': nome,
            'sobrenome': sobrenome,
            'telefone': telefone
        }

        # Cria o voto
        vote = Vote.objects.create(**vote_data)

        # Atualiza o status da pessoa para 'já votou'
        pessoa.ja_votou = True
        pessoa.save()

        return vote

class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['phone_number', 'code', 'is_verified']
        read_only_fields = ['is_verified']

class CandidateResultSerializer(serializers.Serializer):
    candidate_nome = serializers.CharField()
    total_votos = serializers.IntegerField()

class VotantesPercentualSerializer(serializers.Serializer):
    total_pessoas = serializers.IntegerField()
    total_votantes = serializers.IntegerField()
    percentual_votantes = serializers.FloatField()
