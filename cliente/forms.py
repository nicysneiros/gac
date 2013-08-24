from django import forms
from django.forms import ModelForm
from cliente.models import Cliente, Endereco
    
class ClienteForm(ModelForm):
    ID_CHOICES = {
        ('FISICA', 'CPF'),
        ('JURIDICA', 'CNPJ'),
    }

    tipo_identidade = forms.CharField(widget=forms.RadioSelect(choices=ID_CHOICES), label='', initial='FISICA')

    class Meta:
        model = Cliente
        fields = ('nome', 'email', 'telResidencial', 'telCelular', 'id')
        widgets = {
            'nome': forms.TextInput(),
            'email': forms.TextInput(),
            'telResidencial': forms.TextInput(),
            'telCelular': forms.TextInput(),
        }

class EnderecoForm(ModelForm):

    class Meta:
        model = Endereco
        fields = ('logradouro', 'complemento', 'bairro', 'cidade', 'cep')
        widgets = {
            'logradouro': forms.TextInput(),
            'complemento': forms.TextInput(),
            'bairro': forms.TextInput(),
            'cidade': forms.TextInput(),
            'cep': forms.TextInput(),
        }