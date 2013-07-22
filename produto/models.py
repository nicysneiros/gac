from django.db import models

from pedido.models import Servico

# Create your models here.

class Produto (Servico):
    tamanho = models.TextField(blank=True)
    categoria = models.TextField(blank=True)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos/',)

    class Meta:
        db_table = 'Produto'