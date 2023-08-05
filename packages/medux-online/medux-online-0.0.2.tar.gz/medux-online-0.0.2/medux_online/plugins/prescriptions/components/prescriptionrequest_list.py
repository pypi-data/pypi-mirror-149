from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django_unicorn.components import UnicornView

from medux_online.plugins.prescriptions.models import PrescriptionRequest


def check_perm(request, permission: str, obj=None, raise_exception=True):
    if not request:
        raise SystemError("Request not found...")

    if request.user.has_perm(permission, obj=obj):
        return True
    else:
        if raise_exception:
            raise PermissionDenied(
                f"User {request.user.username} doesn't have the '{permission}' permission."
            )


def get_prescriptionrequest_count(request) -> int:
    """Helper function for badge

    :returns: count of open/unresolved prescription requests of current
        tenant
    """
    return PrescriptionRequest.objects.filter(tenant=request.tenant).count()


class PrescriptionrequestListView(PermissionRequiredMixin, UnicornView):
    permission_required = "prescriptions.view_prescriptionrequest"
    template_name = "prescriptions/prescriptionrequest_list.html"
    object_list = PrescriptionRequest.objects.none()

    def mount(self):
        self.update()

    def delete(self, request_id):
        check_perm(self.request, "prescriptions.delete_prescriptionrequest")
        obj = PrescriptionRequest.objects.get(pk=request_id)
        if not obj.tenant == self.request.tenant:
            raise PermissionDenied(
                f"Approval for {self.request.tenant} denied: {obj} belongs to another tenant ({obj.tenant})"
            )
        obj.delete()
        self.update()

    def update(self):
        self.object_list = PrescriptionRequest.objects.filter(
            tenant=self.request.tenant
        )

    def approve(self, id):
        check_perm(self.request, "prescriptions.approve_prescriptionrequest")
        obj = PrescriptionRequest.objects.get(pk=id)
        if not obj.tenant == self.request.tenant:
            # TODO: this error message should not be shown to the
            #  user...is it?
            raise PermissionDenied(
                f"Approval for {self.request.tenant} denied: {obj} belongs to another tenant ({obj.tenant})"
            )
        obj.approved = True
        obj.save()
        self.object_list = PrescriptionRequest.objects.all()
