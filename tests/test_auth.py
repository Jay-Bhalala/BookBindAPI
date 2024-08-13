import unittest
from app import create_app
from flask_jwt_extended import create_access_token

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_protected_route(self):
        # without token
        response = self.client.get('/api/protected')
        self.assertEqual(response.status_code, 401)  # Unauthorized

        # with token
        access_token = create_access_token(identity='testuser@example.com')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = self.client.get('/api/protected', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()