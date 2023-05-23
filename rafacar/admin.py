from django.contrib import admin

from .models import DadosPessoais


@admin.register(DadosPessoais)
class DadosPessoaisAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'telefone', 'cep',
                    'endereco', 'numero_casa', 'bairro', 'cidade')
