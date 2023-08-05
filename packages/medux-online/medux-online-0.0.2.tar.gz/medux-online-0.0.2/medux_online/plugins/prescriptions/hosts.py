from .models import PrescriptionsSite
from ...core.tools import host_patterns_factory

# Dynamically check which sites are PrescriptionSites, and route them
# to the prescriptions' URLCONF.
# this is run once at Django server start, and NOT during mgmt commands.

host_patterns = host_patterns_factory(
    PrescriptionsSite, "medux_online.plugins.prescriptions.root_urls"
)
