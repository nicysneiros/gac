# Create your views here.
from django.http import HttpResponse, QueryDict, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from core.models import *
from django.shortcuts import render, redirect
from django.template import Context, loader
import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from ecrawler.views import crawl

from pedido.models import Pedido, Despesa, Servico
from cliente.models import Cliente
from ecrawler.models import Draft

from pedido.forms import PedidoForm, DespesaForm, CorporativoForm
from django.forms import CharField
import urllib2, urlparse


DATA_TIME_ATUAL = datetime.datetime.now();
DATA_ATUAL = datetime.date.today();


def atualizar_despesa(request):

    if request.POST:
        name = request.POST['name']
        pk = request.POST['pk']
        value = request.POST['value']

        print "ATUALIZACAO DESPESA" + name + " | " + pk + " | " + value

        despesa = Despesa.objects.get(id=pk)

        if name == 'dataCompra':
            dataSplit = value.split('/')
            despesa.data = datetime.date(int(dataSplit[2]), int(dataSplit[1]), int(dataSplit[0]))
            despesa.save()
        elif name == 'descricao':
            despesa.descricao = value
            despesa.save()
        elif name == 'fornecedor':
            despesa.fornecedor = value
            despesa.save()
        elif name == 'valor':
            try:
                valor = float(value)
                despesa.valor = valor
                despesa.save()
            except ValueError:
                return HttpResponseBadRequest('Insira um numero')

    return HttpResponse(content="", status=200)


def remover_despesa(request, id_pedido, id_despesa):

    despesa = Despesa.objects.get(id=id_despesa)
    despesa.delete()

    return redirect('/pedido/detalhe_pedido/' + id_pedido)


def atualizar_pedido(request):

    if request.POST:
        name = request.POST['name']
        pk = request.POST['pk']
        value = request.POST['value']

        print "ATUALIZACAO " + name + " | " + pk + " | " + value

        pedido = Pedido.objects.get(id=pk)

        if name == 'descricao':
            pedido.descricao = value
            pedido.save()
        elif name == 'prazo':
            dataSplit = value.split('/')
            pedido.prazo = datetime.date(int(dataSplit[2]), int(dataSplit[1]), int(dataSplit[0]))
            pedido.save()
        elif name == 'valor':
            try:
                valor = float(value)
                pedido.valor = valor
                pedido.save()
            except ValueError:
                return HttpResponseBadRequest('Insira um numero')

    return HttpResponse(content="", status=200)



def pesquisar_pedido(request):

    if request.POST:
        descricaoPedido = request.POST['descProcurada']
        pedidosAchados = Pedido.objects.filter(descricao__contains=descricaoPedido)

        pedidosAchadosAbertos = []
        pedidosAchadosFechados = []

        for pedido in pedidosAchados:
            
            despesaLista = Despesa.objects.filter(servico=pedido.id)
            pedidoAchado = Pedidos (id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesaLista, desenho=pedido.desenho)
        
            if pedido.prazo > DATA_ATUAL:
                pedidosAchadosAbertos.append(pedidoAchado)
            else:
                pedidosAchadosFechados.append(pedidoAchado)

        crawl()
        drawings = Draft.objects.all()

        retornoAdd = False
        form = PedidoForm()
        corporativoForm = CorporativoForm()

        return render(
            request,
            'pedidos.html',
            {'pedidoAbertoList': pedidosAchadosAbertos,
             'pedidoFechadoList': pedidosAchadosFechados,
             'drawings': drawings,
             'retornoAdd' : retornoAdd,
             'form':form,
             'corporativoForm':corporativoForm})


def remover_pedido(request, id_pedido):

    pedido = Pedido.objects.get(id=id_pedido)
    pedido.delete()

    return redirect('/pedido/info_pedidos/')



@login_required(redirect_field_name='redirect_to')
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



@login_required(redirect_field_name='redirect_to')
def pedidos(request):
    #Gerando a lista de pedidos em aberto mostrados na tabela
    pedidosAbertosLista = Pedido.objects.filter(prazo__gte=DATA_TIME_ATUAL)
    pedidosAbertos = []
    for pedido in pedidosAbertosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoAberto = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista, desenho=pedido.desenho)
        pedidosAbertos.append(pedidoAberto)
    
    #Gerando a lista de pedidos fechados mostrados na tabela
    pedidosFechadosLista = Pedido.objects.filter(prazo__lt=DATA_TIME_ATUAL)
    pedidosFechados = []
    for pedido in pedidosFechadosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoFechado = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista, desenho=pedido.desenho)
        pedidosFechados.append(pedidoFechado)

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
            pedidoAdicionado = form.save(commit=False)

            #print "Descricao Pedido " + pedidoAdicionado.descricao
            #cliente = Cliente.objects.get(id=pedidoAdicionado.cliente.id)

            if request.POST['qtd_P'] != '':
                corporativo = Corporativo()
                corporativo.id = pedidoAdicionado.id
                corporativo.valor = pedidoAdicionado.valor
                corporativo.descricao = "teste hard coded"
                corporativo.data = pedidoAdicionado.data
                corporativo.prazo = pedidoAdicionado.prazo
                corporativo.desenho = pedidoAdicionado.desenho
                corporativo.cliente_id = pedidoAdicionado.cliente.id
                corporativo.qtd_P = request.POST['qtd_P']
                corporativo.qtd_M = request.POST['qtd_M']
                corporativo.qtd_G = request.POST['qtd_G']
                corporativo.save()

            elif request.POST['altura'] != '':
                personalizado = Personalizado(id=pedidoAdicionado.id, valor=pedidoAdicionado.valor, descricao=pedidoAdicionado.descricao, prazo=pedidoAdicionado.prazo, desenho=pedidoAdicionado.desenho)
                personalizado.data = pedidoAdicionado.data
                personalizado.cliente_id = pedidoAdicionado.cliente.id
                personalizado.altura = request.POST['altura']
                personalizado.largura = request.POST['largura']
                personalizado.save()

        retornoAdd = True

    return render(
        request,
        'pedidos.html',
        {'pedidoAbertoList': pedidosAbertos,
         'pedidoFechadoList': pedidosFechados,
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
