# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, loader
import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.shortcuts import redirect


import datetime
from cliente.models import Cliente, Endereco
from pedido.models import Pedido
from produto.models import Produto
from cliente.forms import ClienteForm, EnderecoForm


def pesquisar_cliente(request):

    if request.POST:
        nome = request.POST['clienteProcurado']

        clientes = Cliente.objects.filter(nome__contains=nome)

        clienteForm = ClienteForm()
        enderecoForm = EnderecoForm()
        retornoAdd = False

        return render(request, 'cliente.html', {'clientes': clientes, 'clienteForm': clienteForm, 'enderecoForm': enderecoForm, 'retornoAdd':retornoAdd})


def atualizar_cliente(request):

    if request.POST:
        name = request.POST['name']
        pk = request.POST['pk']
        value = request.POST['value']

        cliente = Cliente.objects.get(id=pk)

        if name == 'nome':
            cliente.nome = value
            cliente.save()
        elif name == 'email':
            cliente.email = value
            cliente.save()
        elif name == 'telResidencial':
            cliente.telResidencial = value
            cliente.save()
        elif name == 'telCelular':
            cliente.telCelular = value
            cliente.save()
        elif name == 'logradouro':
            cliente.endereco.logradouro = value
            cliente.endereco.save()
        elif name == 'complemento':
            cliente.endereco.complemento = value
            cliente.endereco.save()
        elif name == 'bairro':
            cliente.endereco.bairro = value
            cliente.endereco.save()
        elif name == 'cidade':
            cliente.endereco.cidade = value
            cliente.endereco.save()
        elif name == 'cep':
            cliente.endereco.cep = value
            cliente.endereco.save()

    return HttpResponse(content="", status=200)


@login_required(redirect_field_name='redirect_to')
def cliente(request):

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
        cliente.pedidos = Pedido.objects.filter(cliente=cliente.id, prazo__gte=datetime.datetime.now()) 

    # Envia os formularios para adicionar novo cliente e endereco
    clienteForm = ClienteForm()
    enderecoForm = EnderecoForm()

    retornoAdd = False
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
            clienteForm = ClienteForm()
            enderecoForm = EnderecoForm()
        retornoAdd = True

    return render(request, 'cliente.html', {'clientes': clientes, 'clienteForm': clienteForm, 'enderecoForm': enderecoForm, 'retornoAdd':retornoAdd})


@login_required(redirect_field_name='redirect_to')
def detalhe_cliente (request, id_cliente):

    cliente = Cliente.objects.get(id=id_cliente)

    delta = timedelta(days=30)
    dataAtual = datetime.date.today()

    pedidosRecentes = Pedido.objects.filter(cliente_id=cliente.id, prazo__gte=(dataAtual-delta))

    produtosComprados = Produto.objects.filter(cliente_id=cliente.id)

    return render(request, 'detalhe_cliente.html', {'cliente':cliente, 'pedidosRecentes':pedidosRecentes, 'produtosComprados':produtosComprados})
