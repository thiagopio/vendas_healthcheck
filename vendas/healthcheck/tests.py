from django.test import TestCase
from vendas.healthcheck.models import Project, StatusResponse
from django.test.client import Client
import requests_mock


class ProjectTestCase(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='Project Name', environment='DEV')
        StatusResponse.objects.create(project=self.project, url='http://mock.info', status=201, method='GET')
    
    def test_to_json(self):
        json_expected = {'dependents_ids': [], 'id': 1, 'working': False, 'name': 'Project Name', 'status': 404}
        self.assertEqual(self.project.to_json(False), json_expected)

    def test_dependents_size(self):
        self.assertEqual(self.project.dependents_size(), 0)

    def test_in_environment(self):
        self.assertEqual(len(self.project.in_environment('dev')), 1)

    @requests_mock.mock()
    def test_verify(self, mock):
        mock.get('http://mock.info', status_code=202)
        self.assertEqual(self.project.verify(), (False, 202))

class StatusResponseTestCase(TestCase):

    def setUp(self):
        self.status_response = StatusResponse(url='http://mock.info', status=201, method='GET', response_type='STATUS')

    @requests_mock.mock()
    def test_check(self, mock):
        mock.get('http://mock.info', status_code=201)
        self.assertEqual(self.status_response.check(), (True, 201))

    def test_check_exception(self):
        self.status_response.method = 'PUT'
        self.assertRaises(Exception, self.status_response.check())
        self.assertEqual((False, 500), self.status_response.check())

class ViewsTestCase(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='Project Name', environment='DEV')
        StatusResponse.objects.create(project=self.project, url='http://mock.info', status=200, method='GET', response_type='STATUS')
        self.client = Client()

    def test_uri_all_projects(self):
        response = self.client.get('/healthcheck/projects/all/json/')
        json_expected = '{"QA": [], "PROD": [], "DEV": [{"status": 404, "dependents_ids": [], "id": 1, "working": false, "name": "Project Name"}]}'
        self.assertEqual(response.content, json_expected)
    
    @requests_mock.mock()
    def test_uri_a_project(self, mock):
        mock.get('http://mock.info', status_code=200)
        response = self.client.get('/healthcheck/project/1/json/')
        json_expected = '{"status": 200, "dependents_ids": [], "id": 1, "working": true, "name": "Project Name"}'
        self.assertEqual(response.content, json_expected)
