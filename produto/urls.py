from django.conf.urls import patterns, include, url
from django.conf import settings
from produto.views import produtos, detalhe_produto, remover_produto, registrar_venda, add_product, remover_despesa, add_despesa

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^sematrito/', include('core.urls')),
    url(r'^accounts/login/', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
   	url(r'^$', produtos),
   	url(r'^registrar_venda/$', registrar_venda),
   	url(r'^detalhe_produto/(\d+)/$', detalhe_produto),
   	url(r'^detalhe_produto/(\d+)/remove/$', remover_produto),
   	url(r'^add_produto/$', add_product),
    url(r'^detalhe_produto/\d+/remove_despesa/(\d+)$', remover_despesa),
    url(r'^detalhe_produto/(\d+)/add_despesa/$', add_despesa),
)


urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
