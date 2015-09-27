from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=100)
    environment = models.CharField(max_length=10, choices=((0, 'DEV'), (1, 'QA'), (2, 'PROD')))

    def __unicode__(self):
        return self.name
