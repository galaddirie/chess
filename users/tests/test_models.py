from django.test import TestCase
from users.models import Profile
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    """
    Test Module for Users
    """

    def setUp(self) -> None:
        self.user = User.objects.create(
            username='auth_user', email='test@email.com', password='test1234')

    def test_user_profile_created(self):
        self.assertEqual(self.user.profile.is_auth_user(), True)


class ProfileTestCase(TestCase):
    """
    Test Module for Profile Model
    """

    def setUp(self) -> None:
        user = User.objects.create(
            username='auth_user', email='test@email.com', password='test1234')
        self.auth_user = user.profile

        self.anon_user = Profile.objects.create(session_id="anon_user")

    def test_anon_user(self):
        self.assertEqual(self.anon_user.is_auth_user(), False)

    def test_auth_user(self):
        self.assertEqual(self.auth_user.is_auth_user(), True)

    def test_get_profile(self):
        profile = Profile.get_profile('auth_user')
        self.assertEqual(profile.sanitized_name, 'auth_user')

    def test_image_resize(self):
        img = self.auth_user.image
        self.assertTrue(img.height <= 300 or img.width <= 300)

    def test_sanitized_name(self):
        profile = Profile.objects.create(session_id='rANdOm_Caps')
        self.assertEqual(profile.sanitized_name, 'random_caps')
