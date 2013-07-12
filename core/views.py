from django.http import HttpResponse
from core.models import *
from django.shortcuts import render
from django.template import Context, loader

import logging
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

logger = logging.getLogger(__name__)

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

@csrf_protect
def editClientName(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
