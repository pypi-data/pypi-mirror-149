from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured

from medux.common.models import TenantSite


class TenantSiteRequiredMixin(AccessMixin):
    """Mixin that verifies we are on the correct site type (Homepage, etc)."""

    # the site type request.site must have in this view
    site_model: type(TenantSite) = None

    def is_correct_site_type(self):
        """ """
        if self.site_model is None:
            # TODO: print proper error message
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the site_model attribute. Define "
                f"{self.__class__.__name__}.site_model."
            )
        if not issubclass(self.site_model, TenantSite):
            return False
        try:
            self.site_model.objects.get(pk=self.request.site.id)
            return True
        except TenantSite.DoesNotExist:
            return False

    def dispatch(self, request, *args, **kwargs):
        # TODO: maybe don't raise an Error, but a 403
        if not self.is_correct_site_type():
            raise PermissionError(
                f"The view {self.__class__.__name__} can't be accessed from the host {self.request.site}."
            )

        return super().dispatch(request, *args, **kwargs)
