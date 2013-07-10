from django.db import models


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
    # Inserido novo atributo somente para testar ImageField
    # Foto = models.ImageField(upload_to='fotos/', null=True)

    class Meta:
        db_table = 'Cliente'


class Telefone(models.Model):
    numero = models.TextField(primary_key=True)
    clientes = models.ManyToManyField(Cliente, db_column='ID_Clientes')

    class Meta:
        db_table = 'Telefone'

class Servico (models.Model):
    id = models.TextField(primary_key=True)
    valor = models.FloatField(blank=True)
    cliente = models.ForeignKey(Cliente, db_column='ID_Cliente')

    class Meta:
        db_table = 'Servico'


class Produto (Servico):
    # Produto_id = models.OneToOneField(Servico, parent_link=True, db_column='id')
    tamanho = models.TextField(blank=True)
    categoria = models.TextField(blank=True)
    foto = models.ImageField(null=True, blank=True, upload_to='fotos/',)

    class Meta:
        db_table = 'Produto'

class Pedido (Servico):
    # Pedido_id = models.OneToOneField(Servico, parent_link=True, db_column='id')
    descricao = models.TextField(blank=True)
    prazo = models.DateTimeField(blank=True)
    desenho =  models.ImageField(null=True, blank=True, upload_to='desenhos/',)

    class Meta:
        db_table = 'Pedido'

class Corporativo(Pedido):
    # Corporativo_id = models.OneToOneField(Pedido, parent_link=True, db_column='id')
    qtd_P = models.IntegerField(blank=True)
    qtd_M = models.IntegerField(blank=True)
    qtd_G = models.IntegerField(blank=True)

    class Meta:
        db_table = 'Corporativo'

# class Ajuste(Pedido):

class Personalizado(Pedido):
    # Personalizado_id = models.OneToOneField(Pedido, parent_link=True, db_column='id')
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
