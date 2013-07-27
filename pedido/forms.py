from django.forms import ModelForm
from pedido.models import Pedido

class PedidoForm (ModelForm):
	class Meta:
		model = Pedido
		fields = ['valor', 'descricao', 'cliente', 'data', 'prazo', 'desenho']