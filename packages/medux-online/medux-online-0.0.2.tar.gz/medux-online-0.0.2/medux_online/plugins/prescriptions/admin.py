from django.contrib import admin

from medux.common.models import TenantSite
from medux_online.plugins.prescriptions.models import (
    PrescriptionRequest,
    Medication,
    PrescriptionsSite,
)


class MedicationInline(admin.StackedInline):
    model = Medication
    extra = 3


@admin.register(PrescriptionRequest)
class PrescriptionRequestAdmin(admin.ModelAdmin):
    inlines = [MedicationInline]
    list_filter = ["tenant"]


class PrescriptionsSiteAdmin(admin.ModelAdmin):
    pass


class TenantedSiteAdmin(admin.ModelAdmin):
    list_display = ["domain", "name", "tenant"]


admin.site.register(PrescriptionsSite, PrescriptionsSiteAdmin)
admin.site.register(TenantSite, TenantedSiteAdmin)
