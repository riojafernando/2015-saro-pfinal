from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from final.rss import RSS_Principal, Usuarios_RSS

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "final.views.pagina_principal"),
    url(r'^ayuda/$', 'final.views.ayuda'),
    url(r'^register/$', "final.views.nuevo_usuario"),
    url(r'^actividades/(.*)$', "final.views.actividad_concreta"),
    url(r'^logout/$', "final.views.logout"),
    url(r'^css/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL3}),
    url(r'^css/(.*)$', 'final.views.CSS'),
    url(r'^todas/$', 'final.views.lista_actividades'),
    url(r'^root/rss/$', RSS_Principal()),
    url(r'^(.*)/rss/$', Usuarios_RSS()),
    url(r'^(.*)/$', 'final.views.pagina_personal'),
)
