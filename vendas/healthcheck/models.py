# -*- coding: utf-8 -*-
from django.db import models
import requests


class Project(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    environment = models.CharField(max_length=10, choices=(('DEV', 'DEV'), ('QA', 'QA'), ('PROD', 'PROD')))

    @staticmethod
    def in_environment(env):
        return Project.objects.filter(environment=env)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.environment)

    def verify(self):
        try:
            response = requests.get(self.url, timeout=1)
            status = response.status_code
        except Exception as err:
            print 'Problem found in {0}: {1}'.format(self.url, err.message)
            status = 500
        return status

    def to_json(self, with_verify=True):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.verify() if with_verify else 404,
        }
