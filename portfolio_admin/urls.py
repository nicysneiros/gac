from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from portfolio_admin.views import *

urlpatterns = patterns('',
    # Examples:

    url(r'^sematrito/', include('core.urls')),
    url(r'^accounts/login/', include('core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adicionar_portfolio/', adicionar_portfolio),
    url(r'^remover_portfolio/', remover_portfolio),
    url(r'^pesquisar_produto1', buscar_portfolio1),
    url(r'^pesquisar_produto2', buscar_portfolio2),
    url(r'^', portfolio),
)


urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
