from django.forms import ModelForm, CharField, HiddenInput, DateField, ImageField
from pedido.models import Pedido, Despesa
from datetime import datetime
from django.forms.widgets import DateTimeInput

DATE_FORMAT = '%d/%m/%Y'


class FormattedDateInput(DateTimeInput):
	format = DATE_FORMAT


class PedidoForm (ModelForm):
	
	#desenhoStr = ImageField(required=False)
	prazo = DateField(input_formats=[DATE_FORMAT], widget=FormattedDateInput())

	class Meta:
		model = Pedido
		fields = ['valor', 'descricao', 'cliente', 'data', 'prazo']

	def __init__(self, *args, **kwargs):
		super(PedidoForm, self).__init__(*args, **kwargs)
		self.fields ['descricao'].widget.attrs.update({'class':'span5', 'rows':'3'})
		self.fields ['prazo'].widget.attrs.update({'class':'span2', 'size':'16','readonly':''})
		self.fields ['valor'].widget.attrs.update({'class':'span2'})
		self.fields ['cliente'].widget.attrs.update({'class':'span5'})
		self.fields ['cliente'].label_from_instance = lambda obj: "%s"%obj.nome
		#self.fields ['desenhoStr'].widget.attrs.update({'type':'hidden', 'id':'desenho'})
	
class DespesaForm(ModelForm):

	data = DateField(input_formats=[DATE_FORMAT], widget=FormattedDateInput())

	class Meta:
		model = Despesa	
		fields = ['valor', 'fornecedor', 'descricao', 'data']

	def __init__(self, *args, **kwargs):
		super(DespesaForm, self).__init__(*args, **kwargs)
		self.fields['descricao'].widget.attrs.update({'class':'span5', 'row':'3'})
		self.fields['data'].widget.attrs.update({'class':'span2', 'size':'16', 'readonly':''})
		self.fields['valor'].widget.attrs.update({'class':'span2', 'id':'inputValor'})
		self.fields['fornecedor'].widget.attrs.update({'class':'span5', 'id':'inputFornecedor', 'type':'text'})