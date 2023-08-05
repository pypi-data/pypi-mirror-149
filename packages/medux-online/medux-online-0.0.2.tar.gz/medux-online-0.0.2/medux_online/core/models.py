from django.db import models
from django.utils.translation import gettext_lazy as _

from medux.common.models import TenantSite


class ClientManagementSite(TenantSite):
    """A Site that enables users to manage a client's plugins like
    homepage, prescriptions etc.

    If a ClientManagementSite belongs to the Tenant "Admin" (pk 1), it
    can manage all sites. As default, localhost is a
    ClientManagementSite with tenant "Admin".
    """

    class Meta:
        verbose_name = _("Client management site")
        verbose_name_plural = _("Client management sites")


class SiteMixin(models.Model):
    """Mixin that declares a site FK to the model.

    Models with this Mixin belong to a certain TenantSite.
    """

    class Meta:
        abstract = True

    site = models.ForeignKey(TenantSite, on_delete=models.CASCADE)


class TermsAndConditionsPage(SiteMixin, models.Model):
    class Meta:
        verbose_name = _("Terms and conditions page")
        verbose_name_plural = _("Terms and conditions page")

    # TODO: use django-versionfield
    version = models.CharField(max_length=15)

    # TODO: use django-markdownfield etc.
    content = models.TextField()

    def __str__(self):
        return self.version


class PrivacyPage(SiteMixin, models.Model):
    class Meta:
        verbose_name = _("Privacy page")
        verbose_name_plural = _("Privacy pages")

    # TODO: use django-versionfield
    version = models.CharField(max_length=15)

    # TODO: use django-markdownfield etc.
    content = models.TextField()

    def __str__(self):
        return self.version
