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
        working, status = (False, None)
        for expected_response in self.statusresponse_set.all():
            working, status = expected_response.check()
            if working == False:
                return working, status
            # print expected_response.url, expected_response.status, status
        return working, status

    def to_json(self, with_verify=True):
        working, status = self.verify() if with_verify else (False, requests.codes.NOT_FOUND)
        return {
            'id': self.id,
            'name': self.name,
            'status': status,
            'working': working,
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
        working, response = False, None
        try:
            if self.method == 'GET':
                response = requests.get(self.url, timeout=2)
                working, status = self.status_successful(response.status_code)
            else:
                raise Exception("Method '{}' not implemented".format(self.method))

        except Exception as err:
            # print ">> Problem found: {}".format(err)
            working, status = working, requests.codes.SERVER_ERROR
        return working, status

    def status_successful(self, status_from_response):
        if status_from_response == self.status:
            return True, status_from_response
        else:
            return False, status_from_response
