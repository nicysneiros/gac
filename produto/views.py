# Create your views here.
from produto.models import Produto
from pedido.models import Despesa
from cliente.models import Cliente
# from produto.forms import ProdutoForm
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from ecrawler.views import crawl
from ecrawler.models import Draft

import datetime


def produtos(request):

    productList = Produto.objects.all()

    clientList = Cliente.objects.all()

    crawl()
    drawings = Draft.objects.all()

    erros = []
    retornoAdd = False
    form = ProdutoForm()

    if request.POST:
        d = Draft.objects.all().filter(id=request.POST.get('foto',0))
        if d: 
            p = Produto(foto=d[0].photo) 
            form = ProdutoForm(request.POST, instance=p)
        else:
            form = ProdutoForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            
            form.save()
            form = ProdutoForm()
        else:
            print form.errors
        retornoAdd = True   
        
    return render(request,'produtos.html',{"productList": productList, "clienteList" : clientList, 'drawings': drawings, 'erros': erros, 'retornoAdd' : retornoAdd,'form':form})


def registrar_venda(request):
    if request.method == 'POST':
        productId = request.POST['productId']
        clientId = request.POST['selectedClient']
        produto = Produto.objects.get(id = productId)
        cliente = Cliente.objects.get(id = clientId)
        produto.cliente = cliente
        data = (request.POST['data_venda']).replace('-','/')
        produto.data = datetime.datetime.strptime( data + ' 1:00 AM', '%d/%m/%Y %I:%M %p')
        produto.save()

    return HttpResponseRedirect('/produto/')


def add_product(request):

    #Se o usuario adicionou um novo produto
    erros = []
    retornoAdd = False
    form = ProdutoForm()

    if request.POST:
        d = Draft.objects.all().filter(id=request.POST.get('foto',0))
        if d: 
            p = Produto(foto=d[0].photo) 
            form = ProdutoForm(request.POST, instance=p)
        else:
            form = ProdutoForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            
            form.save()
            form = ProdutoForm()
        else:
            print form.errors
        retornoAdd = True        

    #template = loader.get_template('pedidos.html')
    #html = template.render(Context({'pedidoAbertoList': pedidosAbertos, 'pedidoFechadoList': pedidosFechados, 'clienteList': clienteLista, 'drawings': drawings, 'erros': erros, 'retornoAdd' : retornoAdd}))
    #return HttpResponse(html)
    
    productList = Produto.objects.all()

    clientList = Cliente.objects.all()

    drawings = Draft.objects.all()
        
    return render(request,'produtos.html',{"productList": productList, "clienteList" : clientList, 'drawings': drawings, 'erros': erros, 'retornoAdd' : retornoAdd,'form':form})

def add_despesa(request, product_id):
    if request.method == 'POST':
        _descricao = request.POST['descricao']
        _data = (request.POST['data']).replace('-','/')
        _valor = request.POST['valor']
        _fornecedor = request.POST['fornecedor']
        _produto = Produto.objects.get(id = product_id)
        d = Despesa(descricao=_descricao,data=datetime.datetime.strptime( _data + ' 1:00 AM', '%d/%m/%Y %I:%M %p'),valor=_valor,fornecedor=_fornecedor,servico=_produto)
        d.save()


    url = cutPath(request.path,2)


    return HttpResponseRedirect(url)





def detalhe_produto(request, product_id):

    produto = Produto.objects.get(id=product_id)

    despesas = Despesa.objects.filter(servico=produto.id)

    valor_gasto = 0
    for despesa in despesas:
    	valor_gasto += despesa.valor

    return render(request, 'detalhe_produto.html', { "produto" : produto, "despesas" : despesas, "cliente" : produto.cliente, "valor_gasto" : valor_gasto})

def remover_produto(request, product_id):

	Produto.objects.get(id = product_id).delete()

	return HttpResponseRedirect('/produto/')


def remover_despesa(request, despesa_id):
    Despesa.objects.get(id = despesa_id).delete()

    url = cutPath(request.path,2)

    return HttpResponseRedirect(url)



def cutPath(path,n):
    path = path.split('/')

    url = "/"
    for i in range(0,len(path)-n):
        url += "/" + path[i]
    url += "/"

    return url
