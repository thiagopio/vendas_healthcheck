from django.test import TestCase
from vendas.healthcheck.models import Project, StatusResponse
from django.test.client import Client
import requests_mock


class ProjectTestCase(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='Project Name', environment='DEV')
        StatusResponse.objects.create(project=self.project, url='http://mock.info', status=201, method='GET')

    def test_to_json(self):
        json_expected = {'dependents_ids': [], 'id': 1, 'working': False, 'name': 'Project Name', 'info': 404}
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
        self.status_response = StatusResponse(url='http://mock.info', status=201, method='GET',
                                              response_type='STATUS')
        self.text_response = StatusResponse(url='http://mock.info', status=200, method='GET',
                                            response_type='TEXT', content='CONTENT EQUAL')
        self.url_response = StatusResponse(url='http://mock.info', status=200, method='GET',
                                           response_type='URL', content='http://other.info')
        self.regex_response = StatusResponse(url='http://mock.info', status=200, method='GET',
                                             response_type='REGEX', content='<quantidade>(.*)</quantidade>')

    @requests_mock.mock()
    def test_check_regex(self, mock):
        xml_test = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><qtdeFilaProcessar><quantidade>12345</quantidade></qtdeFilaProcessar>'
        mock.get('http://mock.info', status_code=200, text=xml_test)
        self.assertEqual(self.regex_response.check(), (True, '12345'))

    @requests_mock.mock()
    def test_check_url(self, mock):
        mock.get('http://mock.info', status_code=200, text='URL WITH CONTENT EQUAL')
        mock.get('http://other.info', status_code=200, text='URL WITH CONTENT EQUAL')
        self.assertEqual(self.url_response.check(), (True, 'URL WITH CONTENT EQUAL'))

    @requests_mock.mock()
    def test_check_text(self, mock):
        mock.get('http://mock.info', status_code=200, text='CONTENT EQUAL')
        self.assertEqual(self.text_response.check(), (True, 'CONTENT EQUAL'))

    @requests_mock.mock()
    def test_check_status(self, mock):
        mock.get('http://mock.info', status_code=201)
        self.assertEqual(self.status_response.check(), (True, 201))

    def test_check_exception(self):
        self.status_response.method = 'PUT'
        self.assertRaises(Exception, self.status_response.check())
        self.assertEqual((False, 500), self.status_response.check())


class ViewsTestCase(TestCase):

    def setUp(self):
        self.project = Project.objects.create(name='Project Name', environment='DEV')
        StatusResponse.objects.create(project=self.project, url='http://mock.info',
                                      status=200, method='GET', response_type='STATUS')
        self.client = Client()

    def test_uri_all_projects(self):
        response = self.client.get('/healthcheck/projects/all/json/')
        json_expected = '{"QA": [], "PROD": [], "DEV": [{"info": 404, "dependents_ids": [], "id": 1, "working": false, "name": "Project Name"}]}'
        self.assertEqual(response.content, json_expected)

    @requests_mock.mock()
    def test_uri_a_project(self, mock):
        mock.get('http://mock.info', status_code=200)
        response = self.client.get('/healthcheck/project/1/json/')
        json_expected = '{"info": 200, "dependents_ids": [], "id": 1, "working": true, "name": "Project Name"}'
        self.assertEqual(response.content, json_expected)
