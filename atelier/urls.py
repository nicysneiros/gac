from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(r'^sematrito/', include('core.urls')),
    url(r'^accounts/login/', include('core.urls')),


    url(r'^$', include('login.urls')),
    url(r'^login', include('login.urls')),
    url(r'^cliente/', include('cliente.urls')),
    url(r'^pedido/', include('pedido.urls')),
    url(r'^produto/', include('produto.urls')),
    url(r'^portfolio/', include('portfolio.urls')),
    url(r'^portfolio_admin/', include('portfolio_admin.urls')),
    url(r'^relatorio/', include('relatorio.urls')),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
