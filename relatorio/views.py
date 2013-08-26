from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.forms.widgets import DateTimeInput
from pedido.models import Pedido, Despesa, Servico
from produto.models import Produto
from reports import ProdutosReport, PedidosReport
from geraldo.generators import PDFGenerator
from django.shortcuts import redirect
import datetime

DATE_FORMAT = '%d/%m/%Y'
DATA_ATUAL = datetime.date.today();

def relatorio(request):
 form = DateForm()    
 if request.POST:
    dataInicioString = request.POST['dataInicio']
    dataFimString = request.POST['dataFim']
    gerarPDF = request.POST.get('pdf', False)



    dataSplitInicio=dataInicioString.split('/')
    
    dataSplitFim=dataFimString.split('/')    

    global dataInicio, dataFim

    dataInicio=datetime.date(int(dataSplitInicio[2]), int(dataSplitInicio[1]), int(dataSplitInicio[0]))

    dataFim=datetime.date(int(dataSplitFim[2]), int(dataSplitFim[1]), int(dataSplitFim[0]))

    pedidosSelecionadosLista = Pedido.objects.filter(prazo__range=(dataInicio,dataFim))

    lucroPedidosTotal=0

    depesaPedidosTotal=0


    pedidosSelecionados = []   
    for pedido in pedidosSelecionadosLista:
        despesasLista = []
        despesasLista = Despesa.objects.filter(servico=pedido.id)
        lucroPedidosTotal = lucroPedidosTotal + pedido.valor
        pedidosSelecionado = Pedidos(id=pedido.id, dataEntrega=pedido.prazo, descricao=pedido.descricao, cliente=pedido.cliente, valorCobrado=pedido.valor, despesasLista=despesasLista, desenho=pedido.desenho)
        depesaPedidosTotal = depesaPedidosTotal + pedidosSelecionado.valorGasto
        pedidosSelecionados.append(pedidosSelecionado)


    produtoSelecionadosLista = Produto.objects.filter(data__range=(dataInicio,dataFim))

    produtosSelecionados=[]

    lucroProdutosTotal=0

    despesaProdutoTotal=0

    for produto in produtoSelecionadosLista:
        despesasLista=[]
        despesasLista= Despesa.objects.filter(servico=produto.id)
        lucroProdutosTotal = lucroProdutosTotal + produto.valor
        produtoSelecionado = Produtos(id=produto.id, dataVenda=produto.data, descricao=produto.descricao, cliente=produto.cliente, valorCobrado=produto.valor, despesasLista=despesasLista, foto=produto.foto, titulo=produto.titulo)
        despesaProdutoTotal = despesaProdutoTotal + produtoSelecionado.valorGasto
        produtosSelecionados.append(produtoSelecionado)


    SubtotalPedidos = lucroPedidosTotal-depesaPedidosTotal    
    SubtotalProdutos=lucroProdutosTotal-despesaProdutoTotal 

    if gerarPDF:

        resp = HttpResponse(mimetype='application/pdf')

        pedidosReport = PedidosReport(queryset=pedidosSelecionados)

        produtoReport= ProdutosReport(queryset=produtosSelecionados)

        canvas = pedidosReport.generate_by(PDFGenerator,resp,return_canvas=True,)

        produtoReport.generate_by(PDFGenerator,canvas=canvas,)

        return resp
        
        
    else:
        return render(request, 'relatorio.html', {'form' : form,'pedidosList': pedidosSelecionados,'produtoList' : produtosSelecionados,'lucroPedidosTotal' : lucroPedidosTotal,'lucroProdutosTotal' : lucroProdutosTotal, 'depesaPedidosTotal' : depesaPedidosTotal, 'despesaProdutoTotal' : despesaProdutoTotal, 'SubtotalProdutos' : SubtotalProdutos, 'SubtotalPedidos' : SubtotalPedidos })  
 else:
    return render(request, 'relatorio.html',{'form' : form})    




class FormattedDateInput(DateTimeInput):
    format = DATE_FORMAT


class DateForm(forms.Form):
    
    dataInicio =  forms.DateField(input_formats=[DATE_FORMAT], widget=FormattedDateInput())
    dataFim =forms.DateField(input_formats=[DATE_FORMAT], widget=FormattedDateInput())
    pdf=forms.ChoiceField(widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields ['dataInicio'].widget.attrs.update({'class':'span2', 'size':'16','readonly':''})
        self.fields ['dataFim'].widget.attrs.update({'class':'span2', 'size':'16','readonly':''})
        self.fields ['pdf'].widget.attrs.update({'class':'span2', 'size':'16','readonly':''})

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

class Produtos:
    def __init__(self, id,dataVenda, descricao, cliente, valorCobrado, despesasLista, foto, titulo):
        self.id = id
        self.dataVenda = dataVenda
        self.descricao = descricao
        self.cliente = cliente
        self.valorCobrado = valorCobrado
        self.despesaLista = despesasLista
        self.calcularValorGasto(despesasLista)
        self.foto = foto

    
    def calcularValorGasto(self, despesasLista):
        valorGastoTotal = 0
        for despesa in despesasLista: valorGastoTotal = valorGastoTotal + despesa.valor
        self.valorGasto = valorGastoTotal           