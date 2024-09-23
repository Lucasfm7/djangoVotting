# myapp/models.py

from django.db import models
from django.utils import timezone

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

class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        # Define o tempo de expiração para o código (exemplo: 10 minutos)
        expiration_time = self.created_at + timezone.timedelta(minutes=3)
        return timezone.now() > expiration_time

    def __str__(self):
        return f"VerificationCode(phone_number={self.phone_number}, code={self.code})"
