from crispy_forms.helper import FormHelper
from django import forms

from .models import (
    Block,
    Header,
    News,
    OpeningHours,
    Gallery,
    Team,
    Contact,
    Map,
    Footer,
)


class BlockForm(forms.ModelForm):
    """A Basic form that represents a `Block` model

    You can subclass this Form and make more specialized Forms. Just add a `Meta` class
    and specify the `model` there, and the excluded fields, mostly they will be
    `exclude = ["tenant", "content"]`. You don't have to subclass BlockForm.Meta explicitly then.
    """

    class Meta:
        model = Block
        exclude = ["tenant", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False

    #     self.helper.layout = Layout(Row(Column("title"), Column("show_title")))
    #


class HeaderForm(BlockForm):
    class Meta:
        model = Header
        exclude = ["tenant", "content"]


class NewsForm(BlockForm):
    class Meta:
        model = News
        exclude = ["tenant", "content"]


class OpeningHoursForm(BlockForm):
    class Meta:
        model = OpeningHours
        exclude = ["tenant", "content"]


class MapForm(BlockForm):
    class Meta:
        model = Map
        exclude = ["tenant", "content"]


class ContactForm(BlockForm):
    class Meta:
        model = Contact
        exclude = ["tenant", "content"]


class TeamForm(BlockForm):
    class Meta:
        model = Team
        exclude = ["tenant", "content"]


class GalleryForm(BlockForm):
    class Meta:
        model = Gallery
        exclude = ["tenant", "content"]


class FooterForm(BlockForm):
    class Meta:
        model = Footer
        exclude = ["tenant", "content"]


all_forms = {
    "block": BlockForm,
    "header": HeaderForm,
    "map": MapForm,
    "opening_hours": OpeningHoursForm,
    "team": TeamForm,
    "news": NewsForm,
    "gallery": GalleryForm,
    "contact": ContactForm,
    "footer": FooterForm,
}
