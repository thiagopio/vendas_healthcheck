# -*- coding: utf-8 -*-
from django.db import models
import requests


class Project(models.Model):
    name = models.CharField(max_length=50)
    environment = models.CharField(max_length=10, choices=(('DEV', 'DEV'), ('QA', 'QA'), ('PROD', 'PROD')))
    related_project = models.ManyToManyField('Project', blank=True)

    @staticmethod
    def in_environment(env):
        return Project.objects.filter(environment__iexact=env)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.environment)

    def dependents_size(self):
        return len(self.related_project.all())

    def verify(self):
        try:
            for status_response in self.statusresponse_set.all():
                status = status_response.check()
                if status != 200:
                    return status
        except Exception as err:
            print 'Problem found: {}'.format(err.message)
            status = 500
        return status

    def to_json(self, with_verify=True):
        status = self.verify() if with_verify else 404
        return {
            'id': self.id,
            'name': self.name,
            'status': status,
            'dependents_ids': [project.id for project in self.related_project.all()]
        }

class StatusResponse(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    response_type = models.CharField(max_length=10, choices=(('STATUS', 'Status'), ('TEXT', 'Text'),))
    method = models.CharField(max_length=10, choices=(('GET', 'GET'),))
    status = models.PositiveSmallIntegerField(blank=False)
    content = models.CharField(max_length=200, blank=True)

    def check(self):
        try:
            response = requests.get(self.url, timeout=2)
            status = response.status_code
        except Exception as err:
            status = 500

