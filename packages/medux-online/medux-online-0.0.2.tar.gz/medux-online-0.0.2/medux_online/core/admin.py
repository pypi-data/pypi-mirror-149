from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from medux.common.models import User
from medux_online.core.models import ClientManagementSite


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ["name", "codename"]


admin.site.site_header = _("MedUX Online administration")
admin.site.site_title = _("MedUX Online")
admin.site.index_title = _("Medically welcome to MedUX Online")

admin.site.register(Permission, PermissionAdmin)
admin.site.register(User)


class ClientManagementSiteAdmin(admin.ModelAdmin):
    list_display = ["domain", "name", "tenant"]


admin.site.register(ClientManagementSite, ClientManagementSiteAdmin)
