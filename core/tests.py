import re
from urllib.parse import urlsplit

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import UserProfile


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AccountSecurityTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_registration_requires_email_confirmation(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Test',
            'last_name': 'Learner',
            'email': 'learner@example.test',
            'password1': 'Riv3r!Archaeology$2026',
            'password2': 'Riv3r!Archaeology$2026',
            'account_space': 'education',
        })
        self.assertRedirects(response, reverse('verification_pending'))
        user = User.objects.get(email='learner@example.test')
        self.assertFalse(user.is_active)
        self.assertEqual(user.userprofile.user_type, 'student')
        self.assertEqual(len(mail.outbox), 1)

        verification_path = next(
            urlsplit(line).path
            for line in mail.outbox[0].body.splitlines()
            if line.startswith('http://')
        )
        preview = self.client.get(verification_path)
        self.assertEqual(preview.status_code, 200)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

        confirmation = self.client.post(verification_path, {'token': re.search(r'/register/verify/([^/]+)/', verification_path).group(1)})
        self.assertRedirects(confirmation, reverse('login'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_login_cannot_change_the_account_platform(self):
        user = User.objects.create_user(
            username='student@example.test', email='student@example.test', password='A-Strong-Password-2026!'
        )
        UserProfile.objects.update_or_create(user=user, defaults={'user_type': 'student'})
        response = self.client.post(reverse('login'), {
            'username': user.email,
            'password': 'A-Strong-Password-2026!',
            'target_space': 'gis_training',
        })
        self.assertRedirects(response, reverse('dashboard_router'), fetch_redirect_response=False)
        user.userprofile.refresh_from_db()
        self.assertEqual(user.userprofile.user_type, 'student')
        self.assertEqual(self.client.get(reverse('gis:training')).status_code, 403)

    def test_failed_login_attempts_are_limited(self):
        for _ in range(8):
            response = self.client.post(reverse('login'), {'username': 'nobody@example.test', 'password': 'wrong'})
            self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'), {'username': 'nobody@example.test', 'password': 'wrong'})
        self.assertEqual(response.status_code, 429)

    def test_password_reset_page_is_available(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
