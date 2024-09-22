# myapp/models.py

from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    empresa = models.CharField(max_length=255)
    segmento = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Candidate(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome}"

class Vote(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, related_name='vote')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Voto de {self.pessoa.nome} para {self.candidate.nome}"
