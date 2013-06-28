from django.http import HttpResponse
from sematrito.atelier.models import *
from django.template import Context, loader

def index(request):
    clientes = Cliente.objects.all()
    t = loader.get_template('index.html')

    ctx = Context({'clientes': clientes,})

    return HttpResponse(t.render(ctx))
