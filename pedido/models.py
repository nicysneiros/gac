from django.db import models

from cliente.models import Cliente

# Create your models here.

class Servico (models.Model):
    id = models.AutoField(primary_key=True)
    valor = models.FloatField(blank=True)
    cliente = models.ForeignKey(Cliente, db_column='ID_Cliente')

    class Meta:
        db_table = 'Servico'

class Pedido (Servico):
    descricao = models.TextField(blank=True)
    prazo = models.DateTimeField(blank=True)
    desenho =  models.ImageField(null=True, blank=True, upload_to='desenhos/',)

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
    id = models.TextField(primary_key=True)
    valor = models.FloatField()
    fornecedor = models.TextField(blank=True)
    descricao = models.TextField(blank=True)
    servico = models.ForeignKey(Servico, db_column='ID_Servico')

    class Meta:
        db_table = 'Despesa'