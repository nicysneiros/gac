from django import forms
from django.forms import ModelForm
from cliente.models import Cliente, Endereco

# class ClienteForm(forms.Form):

#     nome = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Escreva seu nome'}))
#     email = forms.EmailField(required=False)
#     telResidencial = forms.CharField(required=False, label='Telefone Residencial', initial="Ex: (81) 8888-8888")
#     telCelular = forms.CharField(required=False, label='Telefone Celular')
#     identidade = forms.CharField(label='CPF/CNPJ')
#     tipo_identidade = forms.CharField(widget=forms.RadioSelect(choices=ID_CHOICES), label='', initial='FISICA')
#     endereco = forms.ModelChoiceField(queryset=Endereco.objects.all())
    
class ClienteForm(ModelForm):
    ID_CHOICES = {
        ('FISICA', 'CPF'),
        ('JURIDICA', 'CNPJ'),
    }
    tipo_identidade = forms.CharField(widget=forms.RadioSelect(choices=ID_CHOICES), label='', initial='FISICA')

    class Meta:
        model = Cliente
        fields = ('id', 'nome', 'email', 'telResidencial', 'telCelular')
        widgets = {
            'nome': forms.TextInput(),
            'email': forms.TextInput(attrs={'placeholder': 'exemplo@gmail.com'}),
            'telResidencial': forms.TextInput(),
            'telCelular': forms.TextInput(attrs={'placeholder': 'ex: (81) 8888-8888'}),
        }
        
    # class Meta:
    #     model = Endereco
    #     fields = ('complemento')