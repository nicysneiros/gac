# Create your views here.
from produto.models import Produto
from pedido.models import *
from cliente.models import Cliente
from produto.forms import ProdutoForm
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from ecrawler.views import crawl
from ecrawler.models import Draft
from pedido.forms import DespesaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *

import datetime

@login_required(redirect_field_name='redirect_to')
def pesquisar_produto(request):

    if request.POST:
        descricaoProduto = request.POST['descProcurada']
        productList = Produto.objects.filter(descricao__contains=descricaoProduto)
        clientList = Cliente.objects.all()

        crawl()
        drawings = Draft.objects.all()

        retornoAdd = False
        form = ProdutoForm()


        return render(request,'produtos.html',{"productList": productList, "clienteList" : clientList, 'drawings': drawings,'retornoAdd' : retornoAdd,'form':form})


@login_required(redirect_field_name='redirect_to')
def atualizar_produto(request):

    if request.POST:
        name = request.POST['name']
        pk = request.POST['pk']
        value = request.POST['value']

        print "ATUALIZACAO " + name + " | " + pk + " | " + value

        produto = Produto.objects.get(id=pk)

        if name == 'descricao':
            produto.descricao = value
            produto.save()
        elif name == 'categoria':
            produto.categoria = value
            produto.save()
        elif name == 'tamanho':
            produto.tamanho = value
            produto.save()
        elif name == 'valor':
            produto.valor = value
            produto.save()

    return HttpResponse(content="", status=200)




@login_required(redirect_field_name='redirect_to')
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




@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
def registrar_venda(request):
    if request.method == 'POST':
        productId = request.POST['productId']
        clientId = request.POST['selectedClient']
        valor = request.POST['inputValor']
        produto = Produto.objects.get(id = productId)
        cliente = Cliente.objects.get(id = clientId)
        produto.cliente = cliente
        data = (request.POST['data_venda']).replace('-','/')
        produto.data = datetime.datetime.strptime( data + ' 1:00 AM', '%d/%m/%Y %I:%M %p')
        produto.valor = valor
        produto.save()

    return HttpResponseRedirect('/produto/info_produtos/')


@login_required(redirect_field_name='redirect_to')
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


@login_required(redirect_field_name='redirect_to')
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





@login_required(redirect_field_name='redirect_to')
def detalhe_produto(request, product_id):

    produto = Produto.objects.get(id=product_id)

    despesas = Despesa.objects.filter(servico=produto.id)

    valor_gasto = 0
    for despesa in despesas:
    	valor_gasto += despesa.valor

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

    return render(request, 'detalhe_produto.html', { "produto" : produto, "despesas" : despesas, "cliente" : produto.cliente, "valor_gasto" : valor_gasto, "form":despesaForm, "retornoAddDespesa":retornoAddDespesa})

@login_required(redirect_field_name='redirect_to')
def remover_produto(request, product_id):

	Produto.objects.get(id = product_id).delete()

	return HttpResponseRedirect('/produto/info_produtos/')


@login_required(redirect_field_name='redirect_to')
def remover_despesa(request, produto_id, despesa_id):
    Despesa.objects.get(id = despesa_id).delete()

    #url = cutPath(request.path,2)
    return HttpResponseRedirect("/produto/detalhe_produto/%s"%produto_id)



@login_required(redirect_field_name='redirect_to')
def cutPath(path,n):
    path = path.split('/')

    url = "/"
    for i in range(0,len(path)-n):
        url += "/" + path[i]
    url += "/"

    return url
