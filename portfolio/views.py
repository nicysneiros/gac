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
from pedido.models import *

logger = logging.getLogger(__name__)


def portfolio (request):
    produtos = Produto.objects.filter(portfolio=True)
    return render(request, 'GAC2.html', {'produtos' : produtos})

def filtrar (request):
    produtos = Produto.objects.filter(portfolio=True)
    if request.method == 'POST':
        categ = request.POST['categoria']
        produtos1 = Produto.objects.filter(portfolio=True).filter(categoria__istartswith=categ)
        produtos2 = Produto.objects.filter(portfolio=True).filter(categoria__icontains=categ)
        produtos = produtos1 | produtos2
    return render(request, 'GAC2.html', {'produtos' : produtos})
