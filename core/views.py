from django.http import HttpResponse
from core.models import *
from django.shortcuts import render
from django.template import Context, loader

def index(request):
    clientes = Cliente.objects.all()
    t = loader.get_template('index.html')

    ctx = Context({'clientes': clientes,})

    return HttpResponse(t.render(ctx))

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
