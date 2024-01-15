from flask import url_for
from .base_test import BaseTest

class PortfolioTest(BaseTest):
    def test_view_home(self):
        '''Тестує, чи головна сторінка завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.home'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Home page', response.data)

    def test_view_about(self):
        '''Тестує, чи сторінка портфоліо завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.about'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'About Me', response.data)
            self.assertIn(b'Andriy and I am a young student', response.data)

    def test_view_skills(self):
        '''Тестує, чи сторінка навичок завантажується коректно.'''
        with self.client:
            response = self.client.get(url_for('portfolio.skill'))

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'MY SKILLS', response.data)
            self.assertIn(b'CSS and HTML JS', response.data)
            self.assertIn(b'SQL and MY SQL', response.data)





