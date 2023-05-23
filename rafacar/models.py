from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class DadosPessoais(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=255)
    numero_casa = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Agendamento(models.Model):
    # Permitir que o campo user seja nulo
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dados_pessoais = models.OneToOneField(
        DadosPessoais, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    time = models.TimeField()
    endereco = models.TextField()
    preco = models.TextField(null=True)
    nivel = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"Agendamento em {self.date} às {self.time}"
