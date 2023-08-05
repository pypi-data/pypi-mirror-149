from django.contrib.auth.models import Group

from medux.common.models import User
from medux_online.core.tests import MeduxOnlineTestCase


class HomepageViewsTest(MeduxOnlineTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user1 = User.objects.create_user(username="user1", password="user1")
        site_editors = Group.objects.get(name="Site editors")
        cls.user1.groups.add(site_editors)

    def test_dashboard_permission(self) -> None:
        self.login("user1", "user1")
        response = self.client.get("/dashboard/editor")
        self.assertEqual(200, response.status_code)
