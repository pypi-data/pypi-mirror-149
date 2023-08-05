from django.contrib.auth.models import Group

from medux.common.models import User
from medux_online.core.tests import MeduxOnlineTestCase


class CoreViewsTest(MeduxOnlineTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user1 = User.objects.create_user(username="user1", password="user1")
        site_editors = Group.objects.get(name="Site editors")
        cls.user1.groups.add(site_editors)
        # cls.user2 = User.objects.create_user(
        #     username="user2",
        #     password="user2",
        # )

    def test_login(self) -> None:
        response = self.client.get("/dashboard/")
        self.assertRedirects(response, "/accounts/login/?next=/dashboard/")

        self.assertTrue(self.login("user1", "user1"))

    def test_dashboard_permission(self) -> None:

        response = self.client.get("/dashboard/")
        self.assertRedirects(response, "/accounts/login/?next=/dashboard/")

        self.login("user1", "user1")
        response = self.client.get("/dashboard/")
        self.assertEqual(200, response.status_code)
