from django.test import TestCase
from vendas.healthcheck.models import Project
from django.test.client import Client


class ModelTestCase(TestCase):

	def setUp(self):
		self.project = Project(name='Project Name', url='http://globo.com', environment='DEV')
		self.project.save()
	
	def test_to_json(self):
		json_expected = {'dependents_ids': [], 'id': 1, 'name': 'Project Name', 'status': 404}
		self.assertEqual(self.project.to_json(False), json_expected)

	def test_dependents_size(self):
		self.assertEqual(self.project.dependents_size(), 0)

	def test_in_environment(self):
		self.assertEqual(len(self.project.in_environment('dev')), 1)


class ViewsTestCase(TestCase):

	def setUp(self):
		self.project = Project(name='Project Name', url='http://globo.com', environment='DEV')
		self.project.save()
		self.client = Client()

	def test_uri_all_projects(self):
		response = self.client.get('/healthcheck/projects/all/json/')
		json_expected = '{"QA": [], "PROD": [], "DEV": [{"status": 404, "dependents_ids": [], "id": 1, "name": "Project Name"}]}'
		self.assertEqual(response.content, json_expected)