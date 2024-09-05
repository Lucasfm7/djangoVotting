# myapp/models.py

from django.db import models

class Pessoa(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    empresa = models.CharField(max_length=255)
    segmento = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
