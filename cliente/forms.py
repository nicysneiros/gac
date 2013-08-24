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
        fields = ['nome', 'email', 'telResidencial', 'telCelular', 'id']
        widgets = {
            'nome': forms.TextInput(),
            'email': forms.TextInput(),
            'telResidencial': forms.TextInput(),
            'telCelular': forms.TextInput(),
        }

    def __init__ (self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class':'span5'})
        self.fields['email'].widget.attrs.update({'class':'span5'})
        self.fields['telResidencial'].widget.attrs.update({'class':'span2'})
        self.fields['telCelular'].widget.attrs.update({'class':'span2'})
        self.fields['id'].widget.attrs.update({'class':'span3'})


class EnderecoForm(ModelForm):

    class Meta:
        model = Endereco
        fields = ['logradouro', 'complemento', 'bairro', 'cidade', 'cep']
        widgets = {
            'logradouro': forms.TextInput(),
            'complemento': forms.TextInput(),
            'bairro': forms.TextInput(),
            'cidade': forms.TextInput(),
            'cep': forms.TextInput(),
        }

    def __init__ (self, *args, **kwargs):
        super(EnderecoForm,self).__init__(*args, **kwargs)
        self.fields['logradouro'].widget.attrs.update({'class':'span5'})
        self.fields['complemento'].widget.attrs.update({'class':'span2'})
        self.fields['bairro'].widget.attrs.update({'class':'span3'})
        self.fields['cidade'].widget.attrs.update({'class':'span3'})
        self.fields['cep'].widget.attrs.update({'class':'span2'})