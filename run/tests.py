from django.test import TestCase
from rest_framework.parsers import JSONParser
from io import BytesIO

from .models import Run, FilePath
from storage.models import File


# Create your tests here.
class TestRunAPI(TestCase):
    def setUp(self):
        self.run_1 = Run(start_time='2017-01-15 19:51:06', end_time='2017-01-15T19:51:06Z')
        self.run_1.save()
        self.file_1 = File()
        self.file_1.save()
        self.file_path_1 = FilePath(file=self.file_1, run=self.run_1, is_input=True)
        self.file_path_1.save()

    def test_report_view(self):
        response = self.client.post('/api/run/report', data='{"from_time": "2017-01-15 19:51:06"}',
                                    content_type='application/json')
        data = JSONParser().parse(BytesIO(response.content))[0]
        self.assertTrue('id' in data)
        self.assertTrue('log' in data)
        self.assertTrue('file_path_set' in data)
        self.assertEqual(data['end_time'], '2017-01-15T19:51:06Z')
        self.assertEqual(data['status'], 3)

    def test_create_view_bad_request(self):
        response = self.client.post('/api/run/run',
                                    data='[{"file_path_set":{}}]',
                                    content_type='application/json')
        data = JSONParser().parse(BytesIO(response.content))
        self.assertFalse(data[0]['success'])

    def test_create_view(self):
        response = self.client.post('/api/run/run',
                                    data='[{"files":{"client_1":{"id":"%s","is_input":"True"}}}]' % self.file_1.id,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = JSONParser().parse(BytesIO(response.content))
