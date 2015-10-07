from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^healthcheck/', include('vendas.healthcheck.urls')),
    url(r'^jasmine/', include('django_jasmine.urls')),
    url(r'^$', 'vendas.healthcheck.views.status', name='healthcheck_status'),
]

