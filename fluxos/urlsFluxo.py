from django.conf.urls import patterns, include, url

urlpatterns = patterns('fluxos.views',
    url(r'^$', 'listarFluxos'),
    url(r'^pesquisar/$', 'pesquisarFluxos'),
)