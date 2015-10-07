# -*- coding: utf-8 -*-
from django.contrib import admin
from vendas.healthcheck.models import Project, StatusResponse


class StatusResponseInline(admin.TabularInline):
    model = StatusResponse
    extra = 1
    max_num = 5

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'dependents_size')
    list_filter = ['environment',]
    search_fields = ['name',]
    ordering = ('name',)
    inlines = [StatusResponseInline]


admin.site.register(Project, ProjectAdmin)
