from django.contrib.auth.models import Group

from medux.common.models import User
from medux_online.core.tests import MeduxOnlineTestCase


class PrescriptionViewsTest(MeduxOnlineTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user1 = User.objects.create_user(username="user1", password="user1")
        site_editors = Group.objects.get(name="Prescription editors")
        cls.user1.groups.add(site_editors)

    def test_dashboard_permission(self) -> None:
        response = self.client.get("/dashboard/")
        self.assertEqual(302, response.status_code)

        self.login("user1", "user1")
        response = self.client.get("/dashboard/requests")
        self.assertEqual(200, response.status_code)
