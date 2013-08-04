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

from pedido.models import Pedido, Despesa
from cliente.models import Cliente
from ecrawler.models import Draft

from pedido.forms import PedidoForm
from django.forms import CharField

import urllib2, urlparse

def detalhe_pedido(request, id_pedido):

    pedido = Pedido.objects.get(id=id_pedido)
    despesaLista = Despesa.objects.filter(servico=pedido.id)

    pedidoInfo = Pedidos (id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesaLista, desenho=pedido.desenho)


    return render(request, 'detalhe_pedido.html', {'pedido':pedidoInfo})

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

    clienteLista = Cliente.objects.all()

    #crawl()
    drawings = Draft.objects.all()

    #Se o usuario adicionou um novo pedido
    erros = []
    retornoAdd = False
    form = PedidoForm()
    if request.POST:
        form = PedidoForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            desenhoStr = form.cleaned_data.get('desenhoStr')
            print desenhoStr
            image_url = desenhoStr.split('/')[-1]
            image_data = urllib2.urlopen(image_url, timeout=5)
            form.fields['desenho'] = CharField("/fotos/" + desenhoStr)
            form.save()
            form = PedidoForm()
        else:
            print form.errors
        retornoAdd = True        

    #template = loader.get_template('pedidos.html')
    #html = template.render(Context({'pedidoAbertoList': pedidosAbertos, 'pedidoFechadoList': pedidosFechados, 'clienteList': clienteLista, 'drawings': drawings, 'erros': erros, 'retornoAdd' : retornoAdd}))
    #return HttpResponse(html)
    
    return render(request, 'pedidos.html', {'pedidoAbertoList': pedidosAbertos, 'pedidoFechadoList': pedidosFechados, 'clienteList': clienteLista, 'drawings': drawings, 'erros': erros, 'retornoAdd' : retornoAdd,'form':form})
    
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


def validarDados(request, dataAtual):

        erros = []

        valorStr = request.POST['valor']
        valor = 0

        prazoStr = request.POST['prazo']
        prazo = datetime.datetime.strptime(prazoStr + ' 1:00 AM', '%d/%m/%Y %I:%M %p')

        descricao = request.POST['descricao']

        clienteId = request.POST['cliente']
        cliente = Cliente.objects.get(id=clienteId)

        desenhoUrl = request.POST['desenho']

        pathDesenho = desenhoUrl.split('/')
        desenho = "fotos/" + pathDesenho[-1]
        print desenho

        data = dataAtual

        try:
            valor = float(valorStr)
        except ValueError:
            erros.append("Entrada do campo 'Valor do Pedido' precisa ser um dado numerico")
        
        if (descricao == ""):
            erros.append("O campo 'Descricao do Pedido' e obrigatorio")

        if len(erros) == 0:
            try:
                #Pedido (valor, descricao, Cliente, data, prazo, desenho)
                novoPedido = Pedido (valor=valor, descricao=descricao, cliente=cliente, data=data, prazo=prazo, desenho=desenho)
                novoPedido.save()
            except Exception as e:
                erros.append (e.__str__())

        return erros

        
