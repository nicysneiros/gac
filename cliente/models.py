from django.db import models

# Create your models here.

class Endereco (models.Model):
    logradouro = models.TextField()
    complemento = models.TextField(blank=True)
    bairro = models.TextField()
    cidade = models.TextField()
    cep = models.TextField()

    class Meta:
        db_table = 'Endereco'

class Cliente (models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    nome = models.TextField()
    email = models.EmailField(blank=True)
    endereco = models.ForeignKey(Endereco, db_column='ID_Endereco')
    telResidencial = models.TextField(blank=True)
    telCelular = models.TextField(blank=True)

    # pessoa juridica
    juridico = models.BooleanField()
    

    class Meta:
        db_table = 'Cliente'
