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

from datetime import datetime
from cliente.models import Cliente, Endereco
from pedido.models import Pedido
from produto.models import Produto

def cliente(request):
    # Pega todos os pedidos que ainda estao em aberto

    # Pega o numero de produtos comprados de cada cliente
    clientes = Cliente.objects.all()
    for cliente in clientes:
        cliente.produtos = Produto.objects.filter(cliente=cliente.id)
        cliente.pedidos = Pedido.objects.filter(cliente=cliente.id, prazo__gte=datetime.now()) 
    return render(request, 'cliente.html', {'clientes': clientes})

def detalhe_cliente (request):
    return render(request, 'detalhe_cliente.html', {})

def adicionar(request):
    if request.method == 'POST':
        # Cria o endereco
        e = Endereco()
        e.logradouro = request.POST.get("inputLogradouro")
        e.complemento = request.POST.get("inputComplemento")
        e.bairro = request.POST.get("inputBairro")
        e.cidade = request.POST.get("inputCidade")
        e.cep = request.POST.get("inputCep")
        e.save()

        # Cria o Cliente
        c = Cliente()
        c.id = request.POST.get("inputId")

        if request.POST.get("inputJuridico") == 'false':
            c.juridico = False
        else:
            c.juridico = True

        c.nome = request.POST.get('inputNome')
        c.email = request.POST.get("inputEmail")
        c.telResidencial = request.POST.get("inputTelResidencial")
        c.telCelular = request.POST.get("inputTelCelular")
        c.endereco = e
        c.save()

    return cliente(request)