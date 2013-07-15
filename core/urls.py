from django.conf.urls import patterns, include, url
from django.conf import settings

from core.views import *

from django.contrib.auth import views

urlpatterns = patterns('',

	#url(r'^$', index),
	url(r'bootstrap/$', addClient ),
	url(r'pedidos/$', pedidos ),
	url(r'home/$', views.login, name='login'),
	url(r'^$', views.login, name='login'),
	url(r'clientes/$', cliente),
	url(r'detalhe_pedido/$', detalhe_pedido),
	url(r'produtos/$', produtos),
	url(r'detalhe_produto/$', detalhe_produto),
	url(r'servico/$', servico),
	url(r'detalhe_cliente/$', detalhe_cliente),

	)