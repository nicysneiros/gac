# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.shortcuts import redirect


@login_required(redirect_field_name='redirect_to')
def cliente(request):
        nome_usuario = request.user.get_username()   
        return render(request, 'cliente.html', {'nome_usuario':nome_usuario})


@login_required(redirect_field_name='redirect_to')
def detalhe_cliente (request):
    return render(request, 'detalhe_cliente.html', {})