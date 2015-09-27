from django.contrib import admin
from vendas.healthcheck.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ['environment',]

admin.site.register(Project, ProjectAdmin)
