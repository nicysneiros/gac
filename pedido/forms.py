from django.forms import ModelForm, CharField, HiddenInput, DateTimeField, ImageField
from pedido.models import Pedido
from datetime import datetime


class PedidoForm (ModelForm):
	
	#desenhoStr = ImageField(required=False)

	class Meta:
		model = Pedido
		fields = ['valor', 'descricao', 'cliente', 'data', 'prazo']

	def __init__(self, *args, **kwargs):
		super(PedidoForm, self).__init__(*args, **kwargs)
		self.fields ['descricao'].widget.attrs.update({'class':'span5', 'rows':'3'})
		self.fields ['prazo'].widget.attrs.update({'class':'span2', 'size':'16', 'value':'01/01/2013', 'readonly':''})
		self.fields ['valor'].widget.attrs.update({'class':'span2'})
		self.fields ['cliente'].widget.attrs.update({'class':'span5'})
		self.fields ['cliente'].label_from_instance = lambda obj: "%s"%obj.nome
		#self.fields ['desenhoStr'].widget.attrs.update({'type':'hidden', 'id':'desenho'})
		