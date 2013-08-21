from django.db import models

from cliente.models import Cliente

# Create your models here.

class Servico (models.Model):
    #atributos de servico
    valor = models.FloatField(blank=True)
    descricao = models.TextField()

    #relacao com a entidade cliente. essa e uma relacao opcional
    cliente = models.ForeignKey(Cliente, db_column='ID_Cliente', blank=True, null=True)
    data = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Servico'

class Pedido (Servico):
    prazo = models.DateField(blank=True)
    desenho =  models.ImageField(null=True, blank=True, upload_to='fotos/',)

    class Meta:
        db_table = 'Pedido'

class Corporativo(Pedido):
    qtd_P = models.IntegerField(blank=True)
    qtd_M = models.IntegerField(blank=True)
    qtd_G = models.IntegerField(blank=True)

    class Meta:
        db_table = 'Corporativo'

# class Ajuste(Pedido):

class Personalizado(Pedido):
    altura = models.TextField(blank=True)
    largura = models.TextField(blank=True)

    class Meta:
        db_table = 'Personalizado'

class Despesa(models.Model):
    #atributos de despesa
    valor = models.FloatField()
    fornecedor = models.TextField(blank=True)
    descricao = models.TextField(blank=True)

    #relacao com a entidade servico
    servico = models.ForeignKey(Servico, db_column='ID_Servico')
    data = models.DateTimeField()

    class Meta:
        db_table = 'Despesa'