from django.test import TestCase
from apps.users.models import User


class TestViews(TestCase):

    def setUp(self):
        self.password = 'ArPg44628/**/'
        self.user = User.objects.create(
            email='testsuperuser@gmail.com',
            first_name='User',
            last_name='Test',
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password(self.password)
        self.user.save()

    def test_example(self):
        users = User.objects.all()
        self.assertEquals(users.count(), 1)
