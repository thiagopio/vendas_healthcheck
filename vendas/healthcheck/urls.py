# -*- coding: utf-8 -*-
from django.conf.urls import include, url


urlpatterns = [
    url(r'^projects/all/json/$', 'vendas.healthcheck.views.all_to_json'),
    url(r'^projects/(?P<env>\w+)/json/$', 'vendas.healthcheck.views.projects_for_env_to_json'),
    url(r'^project/(?P<id>[0-9]+)/json/$', 'vendas.healthcheck.views.project_to_json'),
]