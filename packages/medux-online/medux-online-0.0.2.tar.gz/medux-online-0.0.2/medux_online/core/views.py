from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from medux_online.core.models import TermsAndConditionsPage, PrivacyPage


class DashboardView(PermissionRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"
    permission_required = "core.view_clientmanagementsite"


class TenantMixin(ContextMixin, View):
    class Meta:
        abstract = True

    def get_context_data(self, **kwargs):
        return super().get_context_data(tenant=self.request.tenant, **kwargs)

    def form_valid(self, form):
        # override the tenant with the current request's tenant
        # Note: request.tenant is not available here, but using
        # homepage.tenant is valid here.
        form.instance.tenant = self.request.tenant
        form.cleaned_data["tenant_id"] = self.request.tenant.id
        return super().form_valid(form)


class StaticPageView(TenantMixin, TemplateView):
    """Site-aware Base View for static pages like Terms / Privacy, etc.

    You specify a model which will be rendered as page. This model must
     contain a `title`, `version`, and `content` attribute.
     The latest version found is rendered.
     The `title` attribute is also used as page title.

    You can override the `homepage/staticpage.html` template.
    """

    class Meta:
        abstract = True

    model: type(models.Model) = None
    title: str = None

    template_name = "homepage/staticpage.html"

    def get(self, request: HttpRequest, **kwargs):
        # noinspection PyUnresolvedReferences
        obj = (
            self.model.objects.filter(
                tenant=self.model.tenant,
            )
            .order_by("version")
            .last()
        )
        # context = {"title": self.title, "object": object}
        return super().get(
            request,
            template_name=self.template_name,
            title=self.title,
            object=obj,
            **kwargs,
        )


class PrivacyView(StaticPageView):
    model = PrivacyPage
    title = _("Privacy")


class TermsView(StaticPageView):
    model = TermsAndConditionsPage
    title = _("Terms and conditions")
