from flask import url_for
from flask_login import current_user, login_user

from app.auth.models import User
from .base_test import BaseTest

class AuthTest(BaseTest):


    def test_register_view(self):

        '''Тестує, чи правильно завантажується сторінка реєстрації.'''
        with self.client:
            response = self.client.get(url_for('auth.register'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Register', response.data)
            self.assertIn(b'Username', response.data)
            self.assertIn(b'Sign Up', response.data)

    def test_register_post(self):

        '''Тестує, чи реєстрація користувача виконується успішно.'''
        with self.client:
            response = self.client.post(
                url_for('auth.register'),
                data=dict(username='test', email='test@test.com', password='password', confirm_password='password'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Account successfully created', response.data)
        user = User.query.filter_by(email='test@test.com').first()
        self.assertIsNotNone(user)

    def test_login_view(self):

        '''Тестує, чи сторінка входу завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('auth.login'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Password', response.data)
            self.assertIn(b'Remember me', response.data)
            self.assertIn(b'Login', response.data)

    def test_login(self):
        '''Тестує, чи вхід користувача виконується успішно.'''
        with self.client:
            response = self.client.post(
                url_for('auth.login'),
                data=dict(email='user@gmail.com', password='password'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login successful!', response.data)
            self.assertTrue(current_user.is_authenticated)

    def test_logout(self):
        '''Тестує, чи вихід користувача виконується успішно.'''
        with self.client:
            login_user(User.query.filter_by(id=1).first())

            response = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged out', response.data)
            self.assertFalse(current_user.is_authenticated)