# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.shortcuts import redirect


from datetime import datetime
from cliente.models import Cliente, Endereco
from pedido.models import Pedido
from produto.models import Produto
from cliente.forms import ClienteForm, EnderecoForm

def cliente(request):

    if request.method == 'POST':
        clienteForm = ClienteForm(request.POST)
        enderecoForm = EnderecoForm(request.POST)

        cliente_valido = clienteForm.is_valid()
        endereco_valido = enderecoForm.is_valid()

        if cliente_valido and endereco_valido:

            # Salva o novo endereco no BD
            endereco = enderecoForm.save()

            # Salva o novo cliente no BD
            cliente = clienteForm.save(commit=False)

            cliente.endereco = endereco

            tipo_id = clienteForm.cleaned_data.get("tipo_identidade")

            if (tipo_id == 'FISICA'):
                cliente.juridico = False
            else:
                cliente.juridico = True

            cliente.save()

    # Pega as informacoes necessarias para o preenchimento da tabela:
    # 
    #   1. Nome do cliente
    #   2. Telefone celular do cliente
    #   3. Ha pedidos em aberto (True || False)
    #   4. Quantidade de produtos comprados
    #   
    clientes = Cliente.objects.all()
    for cliente in clientes:
        cliente.produtos = Produto.objects.filter(cliente=cliente.id)
        cliente.pedidos = Pedido.objects.filter(cliente=cliente.id, prazo__gte=datetime.now()) 

    # Envia os formularios para adicionar novo cliente e endereco
    clienteForm = ClienteForm()
    enderecoForm = EnderecoForm()

    return render(request, 'cliente.html', {'clientes': clientes, 'clienteForm': clienteForm, 'enderecoForm': enderecoForm})


@login_required(redirect_field_name='redirect_to')
def detalhe_cliente (request):
    return render(request, 'detalhe_cliente.html', {})

# def adicionar(request):
#     if request.method == 'POST':
#         # Cria o endereco
#         e = Endereco()
#         e.logradouro = request.POST.get("inputLogradouro")
#         e.complemento = request.POST.get("inputComplemento")
#         e.bairro = request.POST.get("inputBairro")
#         e.cidade = request.POST.get("inputCidade")
#         e.cep = request.POST.get("inputCep")
#         e.save()

#         # Cria o Cliente
#         c = Cliente()
#         c.id = request.POST.get("inputId")

#         if request.POST.get("inputJuridico") == 'false':
#             c.juridico = False
#         else:
#             c.juridico = True

#         c.nome = request.POST.get('inputNome')
#         c.email = request.POST.get("inputEmail")
#         c.telResidencial = request.POST.get("inputTelResidencial")
#         c.telCelular = request.POST.get("inputTelCelular")
#         c.endereco = e
#         c.save()

#     return cliente(request)
