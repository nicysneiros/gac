from django.conf.urls import patterns, include, url
from django.conf import settings

from core.views import index, addClient, pedidos, home, home2, cliente, detalhe_pedido



urlpatterns = patterns('',

	url(r'^$', index),
	url(r'bootstrap/$', addClient ),
	url(r'pedidos/$', pedidos ),
	url(r'home/$', home2),
	url(r'cliente/$', cliente),
	url(r'detalhe_pedido/$', detalhe_pedido),

	)