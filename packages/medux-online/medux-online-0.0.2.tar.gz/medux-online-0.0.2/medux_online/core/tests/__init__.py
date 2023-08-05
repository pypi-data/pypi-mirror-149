from django.test import TestCase, override_settings
from gdaps.management.commands.initializeplugins import (
    Command as InitializePluginsCommand,
)

from medux.common.management.commands.initialize import Command as InitializeCommand
from medux.common.management.commands.loadsettings import Command as LoadSettingsCommand


@override_settings(SITE_ID=1)
class MeduxOnlineTestCase(TestCase):
    """A Basic Test case every test in MeduxOnline should inherit from.

    It initializes the application"""

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        InitializeCommand().handle()
        InitializePluginsCommand().handle()
        LoadSettingsCommand().handle()

    def login(self, user: str, password: str):
        if not password:
            password = user
        return self.client.login(username=user, password=password)

    def logout(self):
        return self.client.post("/accounts/logout/")
