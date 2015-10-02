# -*- coding: utf-8 -*-
from django.contrib import admin
from vendas.healthcheck.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'url', 'dependependents_size')
    list_filter = ['environment',]
    search_fields = ['name',]
    ordering = ('name',)

admin.site.register(Project, ProjectAdmin)
