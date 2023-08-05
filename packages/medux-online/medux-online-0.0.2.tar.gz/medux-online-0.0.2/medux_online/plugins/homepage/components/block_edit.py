from django_unicorn.components import UnicornView

from medux_online.plugins.homepage.components import UnicornFormMixin
from ..forms import all_forms


class BlockEditView(UnicornFormMixin, UnicornView):
    template_name = "homepage/block_edit.html"

    def __init__(self, **kwargs):
        self.form_class = all_forms[kwargs["name"]]
        super().__init__(**kwargs)

    def updated(self, name, value):
        print(name, value)
