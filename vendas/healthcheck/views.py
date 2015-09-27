from django.shortcuts import render
from vendas.healthcheck.models import Project


def status(request):
    projects = Project.objects.all()
    context = {
        'projects_in_dev': Project.in_environment('DEV'),
        'projects_in_qa': Project.in_environment('QA'),
        'projects_in_prod': Project.in_environment('PROD')
    }

    return render(request, 'healthcheck/status.html', context)