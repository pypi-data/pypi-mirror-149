import logging

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Manager
from django.template.loader import get_template
from django.views.generic import TemplateView

# from medux.common.views import MultipleFormsView
from ..forms import (
    all_forms,
)

logger = logging.getLogger(__file__)


class HomepageView(TemplateView):
    """
    This is a wrapper view, which combines some of other views into one.
    """

    template_name = "homepage/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        homepage = self.request.site.tenantedsite.homepage
        blocklist = []
        weights = []
        blocks = homepage.block_set.all().order_by("weight")

        theme = homepage.theme
        for block in blocks:

            # render each block as an own view...
            template = get_template(f"themes/{theme.slug}/{block.template_name}")
            # fetch standard fields...
            context = {
                "title": block.title,
                "content": block.content,
                "weight": block.weight,
                "show_title": block.show_title,
            }
            # ... and additional fields for polymorphic child models
            for field_name in block.additional_fields:
                field = getattr(block, field_name)
                # if field is a FK, M2M etc., follow that link...
                if isinstance(field, Manager):
                    field = field.all()
                context[field_name] = field
            view = template.render(context, self.request)

            # ... and add it to the context at the correct position
            index = len(weights)
            for i in range(len(weights)):
                if weights[i] > block.weight:
                    index = i
                    break

            blocklist.insert(index, view)
            weights.insert(index, block.weight)

        context["blocks"] = blocklist
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # tenant = request.tenant
        # if tenant:
        #     context["header"] = Header.objects.filter(tenant=tenant).first()
        #     context["homepage"] = Homepage.objects.filter(tenant=tenant).first()
        return super().get(request, context=context, *args, **kwargs)


class EditorView(PermissionRequiredMixin, TemplateView):
    template_name = "homepage/editor.html"
    forms_classes = all_forms
    permission_required = "homepage.change_homepagesite"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["special_blocks"] = []
        context["generic_blocks"] = []
        for (name, form) in self.forms_classes.items():
            if name == "block":
                continue
                # context["generic_blocks"].append({"form":form,"object":})
            else:

                # There must not be more than one here, so first() should be ok
                instance = form._meta.model.objects.filter(
                    homepage__tenant=self.request.tenant
                ).first()
                context["special_blocks"].append(
                    {
                        "name": name,
                        "form": form(instance=instance),
                        "instance": instance,
                    }
                )

        #     if "request" in kwargs:
        #         request = kwargs["request"]
        #
        return context

    #     self.named_blocks = OrderedDict({x: None for x in self.form_classes.keys()})
    #     del self.named_blocks["block"]
    #     generic_blocks = []
    #     for block in Block.objects.filter(
    #         tenant=self.request.tenant
    #     ).order_by("weight"):
    #         btype = block.btype()
    #
    #         if btype == "block":
    #             # ok, multiple generic blocks may exist
    #             generic_blocks.append(
    #                 {
    #                     "block": block,
    #                     "form": BlockForm(instance=block),
    #                 }
    #             )
    #             continue
    #
    #         if btype not in self.named_blocks:
    #             raise IndexError(
    #                 f"Block {block} has an unknown block type: {block.btype()}."
    #             )
    #
    #         if self.named_blocks[btype] is not None:
    #             # should not be, as only one of each block types may exist per tenant!
    #             logger.error(
    #                 f"Found block of type '{btype}' for tenant '{self.request.tenant}'.\n"
    #                 f"This is an error, as only one one '{btype}' block may exist per tenant."
    #             )
    #         else:
    #             self.named_blocks[btype] = {
    #                 "block": block,
    #                 "form": self.form_classes[btype](instance=block),
    #             }
    #
    #     context["named_blocks"] = self.named_blocks
    #     context["generic_blocks"] = generic_blocks
