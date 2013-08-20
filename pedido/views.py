# Create your views here.
from django.http import HttpResponse, QueryDict
from core.models import *
from django.shortcuts import render
from django.template import Context, loader
import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required

from ecrawler.views import crawl

from pedido.models import Pedido, Despesa, Servico
from cliente.models import Cliente
from ecrawler.models import Draft

from pedido.forms import PedidoForm, DespesaForm, CorporativoForm
from django.forms import CharField

import urllib2, urlparse


def detalhe_pedido(request, id_pedido):

    pedido = Pedido.objects.get(id=id_pedido)
    despesaLista = Despesa.objects.filter(servico=pedido.id)

    pedidoInfo = Pedidos (id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesaLista, desenho=pedido.desenho)
    
    retornoAddDespesa = False
    despesaForm = DespesaForm()

    if request.POST:
        idServico = request.POST['servico']
        print "ID: " + idServico
        servico = Servico.objects.get(id=idServico)
        print isinstance(servico, Servico)
        print servico
        despesa = Despesa(servico=servico)
        despesaForm = DespesaForm(request.POST or None, instance=despesa)

        if despesaForm.is_valid():
            despesaForm.save()

        retornoAddDespesa = True

    return render(request,
        'detalhe_pedido.html',
        {'pedido' : pedidoInfo,
         'form' : despesaForm,
          'retornoAddDespesa' : retornoAddDespesa})


def pedidos(request):

    dataAtual = datetime.datetime.now();

    #Gerando a lista de pedidos em aberto mostrados na tabela
    pedidosAbertosLista = Pedido.objects.filter(prazo__gte=dataAtual)
    pedidosAbertos = []
    for pedido in pedidosAbertosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoAberto = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista, desenho=pedido.desenho)
        pedidosAbertos.append(pedidoAberto)
    
    #Gerando a lista de pedidos fechados mostrados na tabela
    pedidosFechadosLista = Pedido.objects.filter(prazo__lt=dataAtual)
    pedidosFechados = []
    for pedido in pedidosFechadosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoFechado = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista, desenho=pedido.desenho)
        pedidosFechados.append(pedidoFechado)

    clientes = Cliente.objects.all()
    clienteLista = {}

    for cliente in clientes:
        clienteLista [cliente.id] = cliente.juridico

    crawl()
    drawings = Draft.objects.all()

    #Se o usuario adicionou um novo pedido
    retornoAdd = False
    form = PedidoForm()
    corporativoForm = CorporativoForm()

    if request.POST:
        d = Draft.objects.get(id=request.POST['desenho'])
        p = Pedido(desenho=d.photo) 
        form = PedidoForm(request.POST or None, instance=p)
        

        if form.is_valid():
           form.save()

        retornoAdd = True

    return render(
        request,
        'pedidos.html',
        {'pedidoAbertoList': pedidosAbertos,
         'pedidoFechadoList': pedidosFechados,
         'clienteList': clienteLista,
         'drawings': drawings,
         'retornoAdd' : retornoAdd,
         'form':form,
         'corporativoForm':corporativoForm})
    

class Pedidos:
    def __init__(self, id, dataEntrega, descricao, cliente, valorCobrado, despesasLista, desenho):
        self.id = id
        self.dataEntrega = str(dataEntrega.day) + "/" + str(dataEntrega.month) + "/" + str(dataEntrega.year)
        self.descricao = descricao
        self.cliente = cliente
        self.valorCobrado = valorCobrado
        self.despesaLista = despesasLista
        self.calcularValorGasto(despesasLista)
        self.desenho = desenho

    def calcularValorGasto(self, despesasLista):
        valorGastoTotal = 0
        for despesa in despesasLista: valorGastoTotal = valorGastoTotal + despesa.valor
        self.valorGasto = valorGastoTotal
