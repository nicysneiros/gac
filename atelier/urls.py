from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sematrito.views.home', name='home'),
    # url(r'^sematrito/', include('sematrito.foo.urls')),

    url(r'^sematrito/$', 'core.views.index'),
    url(r'^sematrito/addClient/$', 'core.views.addClient'),
    url(r'^sematrito/editClientName/$', 'core.views.editClientName'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
