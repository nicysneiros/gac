from django.db import models


class Endereco (models.Model):
    id = models.AutoField(primary_key=True)
    Logradouro = models.TextField()
    Complemento = models.TextField(blank=True)
    Bairro = models.TextField()
    Cidade = models.TextField()
    CEP = models.TextField()

    class Meta:
        db_table = 'Endereco'

class Cliente (models.Model):
    id = models.IntegerField(primary_key=True)
    Nome = models.TextField()
    Email = models.EmailField(blank=True)
    Endereco = models.ForeignKey(Endereco, db_column='ID_Endereco')
    # Inserido novo atributo somente para testar ImageField
    # Foto = models.ImageField(upload_to='fotos/', null=True)

    class Meta:
        db_table = 'Cliente'


class Pessoa_Fisica (Cliente):
    # CPF = models.OneToOneField(Cliente, parent_link=True, db_column='CPF', primary_key=True)

    def get_CPF(self):
        return self.id

# A aplicacao precisa, ainda, verificar uma possivel falha: se existe Cliente registrado no BD com este mesmo 'value'

    def set_CPF(self, value):
        c = Cliente.objects.get(id=self.id)
        print 'Deletando CPF %s de %s' % (c.id, c.Nome)
        c.delete()
        c2 = Cliente(id=value, Nome=c.Nome, Email=c.Email, Endereco=c.Endereco)
        c2.save()
        print "Criando CPF %s de %s" % (c2.id, c2.Nome)
        self.id = value
        self.save()

    CPF = property(get_CPF, set_CPF)

    class Meta:
        db_table = 'Pessoa_Fisica'


class Pessoa_Juridica (Cliente):
    #CNPJ = models.OneToOneField(Cliente, parent_link=True, db_column='CNPJ')

    def get_CNPJ(self):
        return self.id

# A aplicacao precisa, ainda, verificar uma possivel falha: se existe Cliente registrado no BD com este mesmo 'value'

    def set_CNPJ(self, value):
        c = Cliente.objects.get(id=self.id)
        print 'Deletando CNPJ %s de %s' % (c.id, c.Nome)
        c.delete()
        c2 = Cliente(id=value, Nome=c.Nome, Email=c.Email, Endereco=c.Endereco)
        c2.save()
        print "Criando CNPJ %s de %s" % (c2.id, c2.Nome)
        self.id = value
        self.save()

# A aplicacao precisa, ainda, verificar uma possivel falha: se existe Cliente registrado no BD com este mesmo 'value'

    # def del_CNPJ(self):
    #     c = Cliente.objects.get(id=self.id)
    #     print 'Deletando CNPJ %s de %s' % (c.id, c.Nome)
    #     c.delete()
    #     self.delete()

    CNPJ = property(get_CNPJ, set_CNPJ)

    class Meta:
        db_table = 'Pessoa_Juridica'

class Telefone(models.Model):
    Numero = models.TextField(primary_key=True)
    Clientes = models.ManyToManyField(Cliente, db_column='ID_Clientes')

    class Meta:
        db_table = 'Telefone'

class Servico (models.Model):
    id = models.TextField(primary_key=True)
    Valor = models.FloatField(blank=True)
    Cliente = models.ForeignKey(Cliente, db_column='ID_Cliente')

    class Meta:
        db_table = 'Servico'


class Produto (Servico):
    # Produto_id = models.OneToOneField(Servico, parent_link=True, db_column='id')
    Tamanho = models.TextField(blank=True)
    Categoria = models.TextField(blank=True)
    Foto = models.ImageField(null=True, blank=True, upload_to='fotos/',)

    class Meta:
        db_table = 'Produto'

class Pedido (Servico):
    # Pedido_id = models.OneToOneField(Servico, parent_link=True, db_column='id')
    Descricao = models.TextField(blank=True)
    Prazo = models.DateTimeField(blank=True)
    Desenho =  models.ImageField(null=True, blank=True, upload_to='desenhos/',)

    class Meta:
        db_table = 'Pedido'

class Corporativo(Pedido):
    # Corporativo_id = models.OneToOneField(Pedido, parent_link=True, db_column='id')
    Qtd_P = models.IntegerField(blank=True)
    Qtd_M = models.IntegerField(blank=True)
    Qtd_G = models.IntegerField(blank=True)

    class Meta:
        db_table = 'Corporativo'

# class Ajuste(Pedido):

class Personalizado(Pedido):
    # Personalizado_id = models.OneToOneField(Pedido, parent_link=True, db_column='id')
    Altura = models.TextField(blank=True)
    Largura = models.TextField(blank=True)

    class Meta:
        db_table = 'Personalizado'

class Despesa(models.Model):
    id = models.TextField(primary_key=True)
    Valor = models.FloatField()
    Fornecedor = models.TextField(blank=True)
    Descricao = models.TextField(blank=True)
    Servico = models.ForeignKey(Servico, db_column='ID_Servico')

    class Meta:
        db_table = 'Despesa'
