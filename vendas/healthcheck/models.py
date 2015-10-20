# -*- coding: utf-8 -*-
from django.db import models
import requests
import re


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
        working, info = (False, None)
        for expected_response in self.statusresponse_set.all():
            working, info = expected_response.check()
            if working is False:
                return working, info
        return working, info

    def to_json(self, with_verify=True):
        working, info = self.verify() if with_verify else (False, requests.codes.NOT_FOUND)
        return {
            'id': self.id,
            'name': self.name,
            'info': info,
            'working': working,
            'dependents_ids': [project.id for project in self.related_project.all()]
        }


class StatusResponse(models.Model):
    OPTIONS = (('STATUS', 'Status'), ('TEXT', 'Text'), ('URL', 'Other Url'), ('REGEX', 'Regex'))

    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    response_type = models.CharField(max_length=10, choices=OPTIONS)
    method = models.CharField(max_length=10, choices=(('GET', 'GET'),))
    status = models.PositiveSmallIntegerField(blank=False)
    content = models.CharField(max_length=200, blank=True)

    def check(self):
        working, info = False, None
        try:
            if self.method == 'GET':
                response = requests.get(self.url, timeout=2)
                working, info = self.status_successful(response)
            else:
                raise Exception("Method '{}' not implemented".format(self.method))

        except Exception:
            working, info = working, requests.codes.SERVER_ERROR
        return working, info

    def status_successful(self, response):
        status_from_response = response.status_code
        if status_from_response == self.status:
            if self.response_type == 'STATUS':
                return True, status_from_response

            elif self.response_type == 'TEXT':
                same_content = self.content == response.text
                return same_content, response.text

            elif self.response_type == 'URL':
                response_extra = requests.get(self.content, timeout=2)
                same_content = response.text == response_extra.text
                return same_content, response_extra.text

            elif self.response_type == 'REGEX':
                return True, '+{}'.format(re.search(self.content, response.text).group(1))

        return False, status_from_response
