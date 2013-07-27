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
from cliente.models import Cliente
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