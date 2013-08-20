from django.conf.urls import patterns, include, url
from django.conf import settings
from pedido.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'info_pedidos/$', pedidos),
    url(r'detalhe_pedido/(\d+)/$', detalhe_pedido),
    url(r'remover_pedido/(\d+)/$', remover_pedido),
    url(r'pesquisar_pedido/$', pesquisar_pedido),

)


urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
