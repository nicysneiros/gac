from django.http import HttpResponse
from core.models import *
from django.shortcuts import render
from django.template import Context, loader
import datetime

def index(request):
    clientes = Cliente.objects.all()

    return render(request,'index.html', {'clientes': clientes,})

def insertClient(request):
    if request.method == 'POST':
        e = Endereco.objects.get(id=1)
        c = Client()
        c.Nome = request.POST.get('nome')
        c.Email = request.POST.get("email")
        c.id = request.POST.get("CPF")
        c.Endereco_id = e.id
        c.save()

    clientes = Cliente.objects.all()

    return render(request, 'index.html', locals())

def pedidos(request):
    dataAtual = datetime.datetime.now();
    
    #Gerando a lista de pedidos em aberto mostrados na tabela
    pedidosAbertosLista = Pedido.objects.filter(prazo__gte=dataAtual)
    pedidosAbertos = []
    for pedido in pedidosAbertosLista:
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoAberto = Pedidos(dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente.nome, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosAbertos.append(pedidoAberto)
        print pedidosAbertos

    #Gerando a lista de pedidos fechados mostrados na tabela
    pedidosFechadosLista = Pedido.objects.filter(prazo__lt=dataAtual)
    pedidosFechados = []
    for pedido in pedidosFechadosLista:
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoFechado = Pedidos(dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente.nome, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosFechados.append(pedidoFechado)

    return render(request, 'pedidos.html',{'pedidoAbertoList': pedidosAbertos, 'pedidoFechadosList': pedidosFechados})

class Pedidos:
    def __init__(self, dataEntrega, descricao, cliente, valorCobrado, despesasLista):
        self.dataEntrega = str(dataEntrega.day) + "/" + str(dataEntrega.month) + "/" + str(dataEntrega.year)
        self.descricao = descricao
        self.cliente = cliente
        self.valorCobrado = valorCobrado
        self.calcularValorGasto(despesasLista)

    def calcularValorGasto(self, despesasLista):
        valorGastoTotal = 0
        for despesa in despesasLista: valorGastoTotal = valorGastoTotal + despesa.valor
        self.valorGasto = valorGastoTotal
