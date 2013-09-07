from django.conf.urls import patterns, include, url
from django.conf import settings

from cliente.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
  
    url(r'info_clientes/$', cliente),
    url(r'detalhe_cliente/(\d+)/$', detalhe_cliente),
    url(r'atualizar_cliente/$', atualizar_cliente),
    url(r'pesquisar_cliente/$', pesquisar_cliente),


)


urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
