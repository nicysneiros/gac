from django.db import models

# Create your models here.

class Endereco (models.Model):
    id = models.AutoField(primary_key=True)
    logradouro = models.TextField()
    complemento = models.TextField(blank=True)
    bairro = models.TextField()
    cidade = models.TextField()
    cep = models.TextField()

    class Meta:
        db_table = 'Endereco'

class Cliente (models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    nome = models.TextField()
    email = models.EmailField(blank=True)
    endereco = models.ForeignKey(Endereco, db_column='ID_Endereco')
    # Inserindo uma variavel booleana para identificar se o cliente e pessoa juridica ou nao
    juridico = models.BooleanField()

    class Meta:
        db_table = 'Cliente'


class Telefone(models.Model):
    numero = models.TextField(primary_key=True)
    clientes = models.ManyToManyField(Cliente, db_column='ID_Clientes')

    class Meta:
        db_table = 'Telefone'