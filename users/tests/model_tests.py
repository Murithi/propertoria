from unittest import TestCase
from django.contrib.auth.models import User
from django_dynamic_fixture import G
from ..models import Profile


class UserModelTests(TestCase):
    def test_users_model_unicode(self):
        user = G(User)
        user_profile = Profile.objects.create(user=user, company='Homesoko')
        self.assertEqual(str(user_profile), 'User: ' + str(user) + ', Company: Homesoko')
