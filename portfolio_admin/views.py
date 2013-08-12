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

def portfolio (request):
    produtos = Produto.objects.all()
    return render(request, 'portfolio.html', {'produtos' : produtos})
	
def portfolio_admin (request):
    produtos = Produto.objects.all()
    return render(request, 'portfolio.html', {'produtos' : produtos})
    
def adicionar_portfolio (request):
    if request.method == 'POST':
        produtos = Produto.objects.all()
        for pp in produtos:
            print pp.portfolio
        print "\n"
        p = Produto.objects.get(id=request.POST['id'])
        p.portfolio = True
        p.save(force_update=True)
        produtos = Produto.objects.all()
        for pp in produtos:
            print pp.portfolio
        print "\n"
    return render(request, 'redirect.html', {})
    
def remover_portfolio (request):
    if request.method == 'POST':
        produtos = Produto.objects.all()
        for pp in produtos:
            print pp.portfolio
        print "\n"
        p = Produto.objects.get(id=request.POST['id'])
        p.portfolio = False
        p.save(force_update=True)
        produtos = Produto.objects.all()
        for pp in produtos:
            print pp.portfolio
        print "\n"
    return render(request, 'redirect.html', {})