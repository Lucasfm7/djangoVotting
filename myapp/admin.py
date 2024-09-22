# myapp/admin.py

from django.contrib import admin
from .models import Pessoa, Candidate, Vote

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'empresa', 'segmento']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['nome']  # Removido 'partido'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['pessoa', 'candidate', 'timestamp']
