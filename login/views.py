from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import views
from django.contrib.auth import *
from django.shortcuts import render



def logout_user(request):
    logout(request)
    return redirect('/')

def login_user(request):
    logado = request.user.is_authenticated()
    if not logado:
        return views.login(request)
    else:
        nome_usuario = request.user.get_username()   
        return render(request, 'registration/login.html', {'nome_usuario':nome_usuario, 'logado':logado})  



