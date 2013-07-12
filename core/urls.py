from django.conf.urls import patterns, include, url
from django.conf import settings

from core.views import index, insertClient, pedidos



urlpatterns = patterns('',

	url(r'^$', index),
	url(r'bootstrap/$', insertClient ),
	url(r'pedidos/$', pedidos ),
	)