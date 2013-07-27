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
from ecrawler.models import Draft

logger = logging.getLogger(__name__)


def home(request):
    return render(request,'GAC2.html', {"lol" : "l"})

@csrf_protect
def index(request):

    linhas = []

    clientes = Cliente.objects.all()

    for cliente in clientes:
        telefones = cliente.telefone_set.all()
        linha = {'cliente': cliente, 'telefones': telefones, }
        linhas.append(linha)

    return render_to_response('index.html', {'linhas': linhas, }, context_instance=RequestContext(request))


# Obs.: Note que falta validar os dados passados pelo usuario. Parte da validacao poderia ser feita no nivel da aplicacao.
# 
# Obs.2: Precisa criar o campo "ehJuridico" no formulario para adicionar um novo Cliente

@csrf_protect
def addClient(request):

    if request.method == 'POST':
        # Cria o endereco
        e = Endereco()
        e.logradouro = request.POST.get("logradouro")
        e.complemento = request.POST.get("complemento")
        e.bairro = request.POST.get("bairro")
        e.cidade = request.POST.get("cidade")
        e.cep = request.POST.get("cep")
        e.save()

        # Cria o Cliente
        c = Cliente()
        c.id = request.POST.get("id")
        c.nome = request.POST.get('nome')
        c.email = request.POST.get("email")
        c.endereco = e
        c.juridico = True
        c.save()

        # Cria o telefone
        celular = Telefone()
        celular.numero = request.POST.get("celular")
        celular.save()

        fixo = Telefone()
        fixo.numero = request.POST.get("residencial")
        fixo.save()

        # Associa o telefone ao Cliente
        celular.clientes.add(c)
        fixo.clientes.add(c)

    return index(request)

@login_required(redirect_field_name='redirect_to')
def pedidos(request):
    dataAtual = datetime.datetime.now();
    
    #Gerando a lista de pedidos em aberto mostrados na tabela
    pedidosAbertosLista = Pedido.objects.filter(prazo__gte=dataAtual)
    pedidosAbertos = []
    for pedido in pedidosAbertosLista:
        despesasLista = []
        #despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoAberto = Pedidos(dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente.nome, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosAbertos.append(pedidoAberto)
        print pedidosAbertos

    #Gerando a lista de pedidos fechados mostrados na tabela
    pedidosFechadosLista = Pedido.objects.filter(prazo__lt=dataAtual)
    pedidosFechados = []
    for pedido in pedidosFechadosLista:
        despesasLista = []
        #despesasLista = Despesa.objects.filter(servico=pedido.id)
        pedidoFechado = Pedidos(dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente.nome, valorCobrado=pedido.valor, despesasLista=despesasLista)
        pedidosFechados.append(pedidoFechado)

    clienteLista = Cliente.objects.all()

    for cliente in clienteLista: print cliente.nome


    drawings = Draft.objects.all()
    return render(request, 'pedidos.html',{'pedidoAbertoList': pedidosAbertos, 'pedidoFechadosList': pedidosFechados, 'clienteList': clienteLista, "drawings" : drawings})

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

@csrf_protect
def editClientName(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))



def home2(request):
    return render(request,'home_admin.html',{})


def cliente(request):
    return render(request, 'cliente.html', {})

def detalhe_pedido(request):
    return render(request, 'detalhe_pedido.html', {})

def detalhe_produto(request):
    return render(request, 'detalhe_produto.html', {})

def servico (request):
    return render(request, 'servico.html', {})

def detalhe_cliente (request):
    return render(request, 'detalhe_cliente.html', {})

def portfolio (request):
    return render(request, 'portfolio.html', {})

def relatorio (request):
    return render(request, 'relatorio.html', {})

def produtos(request):
    print 'lolProdutos'
    if request.method == 'POST':
        print request.POST['productId']
        
    return render(request,'produtos.html',{})

