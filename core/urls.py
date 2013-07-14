from django.conf.urls import patterns, include, url
from django.conf import settings

from core.views import index, addClient, pedidos, home, home2, cliente, detalhe_pedido

from django.contrib.auth import views

urlpatterns = patterns('',

	#url(r'^$', index),
	url(r'bootstrap/$', addClient ),
	url(r'pedidos/$', pedidos ),
	url(r'home/$', views.login, name='login'),
	url(r'^$', views.login, name='login'),
	url(r'cliente/$', cliente),
	url(r'detalhe_pedido/$', detalhe_pedido),

	)