# Create your views here.
from django.http import HttpResponse
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

from pedido.models import Pedido, Despesa
from cliente.models import Cliente
from ecrawler.models import Draft

from pedido.forms import PedidoForm


def detalhe_pedido(request, id_pedido):

    pedido = Pedido.objects.get(id=id_pedido)
    despesaLista = Despesa.objects.filter(servico=pedido.id)

    pedidoInfo = Pedidos (id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesaLista)


    return render(request, 'detalhe_pedido.html', {'pedido':pedidoInfo})

def pedidos(request):

    dataAtual = datetime.datetime.now();

    #Se o usuario adicionou um novo pedido
    if request.POST:

        erros = []
        valor = 0
        prazo = datetime.datetime.strptime((request.POST['prazo']) + ' 1:00 AM', '%d/%m/%Y %I:%M %p')
        descricao = ""
        cliente = Cliente.objects.get(id=(request.POST['cliente']))
        data = dataAtual
        desenho = request.POST['desenho']

        if 'valor' in request.POST:
            valorStr = request.POST['valor']
            try:
                valor = float(valorStr)
            except exceptions.ValueError:
                erros.append("Entrada do campo 'Valor do Pedido' precisa ser um dado numérico")
        else:
            erros.append("O campo 'Valor do Pedido' é obrigatório")

        if 'descricao' in request.POST:
            descricao = request.POST['descricao']
        else:
            erros.append("O campo 'Descrição do Pedido' é obrigatório")

        if erros.length > 0:
            #Pedido (valor, descricao, Cliente, data, prazo, desenho)
            novoPedido = Pedido (valor=valor, descricao=descricao, cliente=cliente, data=data, prazo=prazo, desenho=desenho)
            novoPedido.save()
            
    
    #Gerando a lista de pedidos em aberto mostrados na tabela
    pedidosAbertosLista = Pedido.objects.filter(prazo__gte=dataAtual)
    pedidosAbertos = []
    for pedido in pedidosAbertosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoAberto = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosAbertos.append(pedidoAberto)
        print pedidosAbertos

    #Gerando a lista de pedidos fechados mostrados na tabela
    pedidosFechadosLista = Pedido.objects.filter(prazo__lt=dataAtual)
    pedidosFechados = []
    for pedido in pedidosFechadosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoFechado = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosFechados.append(pedidoFechado)

    clienteLista = Cliente.objects.all()

    crawl()
    drawings = Draft.objects.all()

    return render(request, 'pedidos.html',{'pedidoAbertoList': pedidosAbertos, 'pedidoFechadoList': pedidosFechados, 'clienteList': clienteLista, 'drawings':drawings})

class Pedidos:
    def __init__(self, id, dataEntrega, descricao, cliente, valorCobrado, despesasLista):
        self.id = id
        self.dataEntrega = str(dataEntrega.day) + "/" + str(dataEntrega.month) + "/" + str(dataEntrega.year)
        self.descricao = descricao
        self.cliente = cliente
        self.valorCobrado = valorCobrado
        self.despesaLista = despesasLista
        self.calcularValorGasto(despesasLista)

    def calcularValorGasto(self, despesasLista):
        valorGastoTotal = 0
        for despesa in despesasLista: valorGastoTotal = valorGastoTotal + despesa.valor
        self.valorGasto = valorGastoTotal

