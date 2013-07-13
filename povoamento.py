from core.models import *

#para rodar, abra python manage.py shell, e digite execfile('povoamento.py')


for i in range(0,5):
	e = Endereco(i, 'logradouro%d'%i,'complemento%d'%i,'bairro%d'%i,'cidade%d'%i,'cep%d'%i)
	c = Cliente(i, 'nome%d'%i, 'email@email.com%d'%i,e.id, False)
	p = Produto(i,150,c.id,'mm','categoria','abc/')
	d = Despesa(i,10,'abc','desc',p.id)
	e.save()
	c.save()
	p.save()
	d.save()