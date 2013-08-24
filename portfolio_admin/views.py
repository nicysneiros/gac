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
from ecrawler.models import Draft
from produto.models import *

logger = logging.getLogger(__name__)


@login_required(redirect_field_name='redirect_to')
def portfolio (request):
    produtos = Produto.objects.all()
    return render(request, 'portfolio.html', {'produtos' : produtos})


@login_required(redirect_field_name='redirect_to')	
def portfolio_admin (request):
    produtos = Produto.objects.all()
    return render(request, 'portfolio.html', {'produtos' : produtos})
 
@login_required(redirect_field_name='redirect_to')   
def adicionar_portfolio (request):
    if request.method == 'POST':
        produtos = Produto.objects.all()
        p = Produto.objects.get(id=request.POST['id'])
        p.portfolio = True
        p.save(force_update=True)
        produtos = Produto.objects.all()
    return render(request, 'redirect.html', {})

@login_required(redirect_field_name='redirect_to')    
def remover_portfolio (request):
    if request.method == 'POST':
        produtos = Produto.objects.all()
        p = Produto.objects.get(id=request.POST['id'])
        p.portfolio = False
        p.save(force_update=True)
        produtos = Produto.objects.all()
    return render(request, 'redirect.html', {})
    
@login_required(redirect_field_name='redirect_to')    
def buscar_portfolio1 (request):
    produtos = Produto.objects.all()
    if request.method == 'POST':
        desc = request.POST['descProcurada']
        produtos1 = Produto.objects.filter(descricao__contains=desc)
        produtos2 = Produto.objects.filter(portfolio=False)
        
        produtos = produtos1 | produtos2
        
    return render(request, 'portfolio.html', {'produtos' : produtos, 'modal' : False})
    
def buscar_portfolio2 (request):
    produtos = Produto.objects.all()
    if request.method == 'POST':
        desc = request.POST['descProcurada']
        produtos1 = Produto.objects.filter(descricao__contains=desc)
        produtos2 = Produto.objects.filter(portfolio=True)
        
        produtos = produtos1 | produtos2
        
    return render(request, 'portfolio.html', {'produtos' : produtos, 'modal' : True})


