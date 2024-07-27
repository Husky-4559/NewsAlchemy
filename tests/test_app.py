import unittest
from flask_testing import TestCase
from app import create_app, db
from models import User, Favorite
from config import TestConfig

class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()
        self._ctx = self.app.app_context()
        self._ctx.push()

        # Create a test user
        user = User(username='testuser', email='testuser@example.com')
        user.set_password('Password123!')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self._ctx.pop()

class AuthTestCase(BaseTestCase):
    def test_register(self):
        response = self.client.post('/auth/register', data=dict(
            username='newuser',
            email='newuser@example.com',
            password='Password123!',
            confirm_password='Password123!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully!', response.data)

    def test_login(self):
        response = self.client.post('/auth/login', data=dict(
            username='testuser',
            password='Password123!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful!', response.data)

    def test_login_invalid_password(self):
        response = self.client.post('/auth/login', data=dict(
            username='testuser',
            password='WrongPassword!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Unsuccessful. Please check username and password', response.data)

class FavoriteTestCase(BaseTestCase):
    def login(self):
        self.client.post('/auth/login', data=dict(
            username='testuser',
            password='Password123!'
        ), follow_redirects=True)

    def test_add_favorite(self):
        self.login()
        response = self.client.post('/favorites', json=dict(
            title='Test Article',
            url='http://example.com'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Article added to favorites!', response.data)

    def test_add_duplicate_favorite(self):
        self.login()
        self.client.post('/favorites', json=dict(
            title='Test Article',
            url='http://example.com'
        ))
        response = self.client.post('/favorites', json=dict(
            title='Test Article',
            url='http://example.com'
        ))
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Article already in favorites.', response.data)

    def test_delete_favorite(self):
        self.login()
        response = self.client.post('/favorites', json=dict(
            title='Test Article',
            url='http://example.com'
        ))
        favorite_id = response.json['favorite']['id']
        response = self.client.delete(f'/favorites?id={favorite_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Favorite deleted.', response.data)

if __name__ == '__main__':
    unittest.main()