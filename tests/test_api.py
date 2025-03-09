import unittest
from flask import json
from backend.app import app  # Ensure this import is correct
import numpy as np

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_predict(self):
        response = self.client.post('/predict', 
                                     data=json.dumps({'input': [[1, 2], [3, 4]]}), 
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.get_json())

if __name__ == '__main__':
    unittest.main()