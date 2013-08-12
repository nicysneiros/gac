from django import forms
from produto.models import Produto
from django.forms import ModelForm

class ContactForm(forms.Form):
    subject = forms.CharField(widget = forms.Textarea)
    email = forms.EmailField(required=False)
    message = forms.CharField()

class ProdutoForm (ModelForm):

	class Meta:
		model = Produto
		fields = ['descricao', 'categoria','tamanho','valor']

	def __init__(self, *args, **kwargs):
		super(ProdutoForm, self).__init__(*args, **kwargs)
		self.fields['descricao'].widget.attrs.update({'class':'span5', 'rows':'3'})
		#self.fields['categoria'].widget = forms.TextInput(attrs={'class':'span3'})
		self.fields['categoria'].widget.attrs.update({'class':'span3'})
		self.fields['tamanho'].widget.attrs.update({'class':'span2'})
		#self.fields['tamanho'].widget = forms.TextInput(attrs={'class':'span2'})
		#self.fields['valor'].widget = forms.NumberInput(attrs={'class':'span2'})
		self.fields ['valor'].widget.attrs.update({'class':'span2'})

