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

# myapp/serializers.py

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
        # Since the validations are in the view, simply create the vote
        cpf = validated_data.pop('cpf')
        candidate_id = validated_data.pop('candidate_id')
        pessoa = Pessoa.objects.get(cpf=cpf)
        candidate = Candidate.objects.get(id=candidate_id)

        vote = Vote.objects.create(
            pessoa=pessoa,
            candidate=candidate,
            nome=validated_data.get('nome'),
            sobrenome=validated_data.get('sobrenome'),
            telefone=validated_data.get('telefone')
        )

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
