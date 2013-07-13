from django.conf.urls import patterns, include, url
from django.conf import settings

from core.views import index, addClient, pedidos, home



urlpatterns = patterns('',

	url(r'^$', index),
	url(r'bootstrap/$', addClient ),
	url(r'pedidos/$', pedidos ),
	url(r'home/$', home),
	)