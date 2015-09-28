# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from vendas.healthcheck.models import Project
from django.shortcuts import get_object_or_404
import json


def status(request):
    return render(request, 'healthcheck/status.html')

def all_to_json(request):
    response = {
        'DEV': [project.to_json(False) for project in Project.in_environment('DEV')],
        'QA': [project.to_json(False) for project in Project.in_environment('QA')],
        'PROD': [project.to_json(False) for project in Project.in_environment('PROD')]
    }
    return HttpResponse(json.dumps(response), content_type="application/json")

def projects_for_env_to_json(request, env):
    return HttpResponse(json.dumps({}), content_type="application/json")

def project_to_json(request, id):
    project = get_object_or_404(Project, pk=id)
    return HttpResponse(json.dumps(project.to_json()), content_type="application/json")
