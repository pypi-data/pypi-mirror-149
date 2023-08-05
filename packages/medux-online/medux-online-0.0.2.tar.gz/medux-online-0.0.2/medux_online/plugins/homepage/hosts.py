from .models import HomepageSite
from ...core.tools import host_patterns_factory

# Dynamically check which sites are HomepageSites, and route them
# to the Homepage's URLCONF.
# this is run once at Django server start, and NOT during mgmt commands.

host_patterns = host_patterns_factory(
    HomepageSite, "medux_online.plugins.prescriptions.root_urls"
)
