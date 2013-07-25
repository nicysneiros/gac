from core.models import *
from random import randrange
from datetime import timedelta
from random import randint
from datetime import datetime

def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))

#para rodar, abra python manage.py shell, e digite execfile('povoamento.py')

Endereco.objects.all().delete()
Cliente.objects.all().delete()
Produto.objects.all().delete()
Despesa.objects.all().delete()
Pedido.objects.all().delete()


startDate = datetime.strptime('19/07/2013 1:30 PM', '%d/%m/%Y %I:%M %p')
endDate = datetime.strptime('28/07/2013 1:30 PM', '%d/%m/%Y %I:%M %p')

for i in range(0,10):
	e = Endereco(i, 'logradouro%d'%i,'complemento%d'%i,'bairro%d'%i,'cidade%d'%i,'cep%d'%i)
	c = Cliente(i, 'nome%d'%i, 'email@email.com%d'%i,e.id, False)
	p = Produto(i,150,c.id,'mm','categoria','abc/')
	d = Despesa(i,10,'abc','desc',p.id)
	data = random_date(startDate,endDate)
	pe = Pedido(i,100,c.id,'descPedido','descPedido',data)
	e.save()
	c.save()
	p.save()
	d.save()
	pe.save()
