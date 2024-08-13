import unittest
from app import create_app
from flask import json

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_register_user(self):
        response = self.client.post('/api/users/register', json={
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post('/api/users/login', json={
            'email': 'testuser@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_fetch_books(self):
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()