from pathlib import Path

from colorfield.fields import ColorField
from django.core.files.storage import Storage
from django.core.validators import MinValueValidator, MaxValueValidator, validate_slug
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from medux.common.models import TenantSite
from medux.settings.models import ScopedSettings


# from zipfile import ZipFile


# # thanks to https://goodcode.io/articles/django-singleton-models/
# class SingletonModel(models.Model):
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         self.__class__.objects.exclude(id=self.id).delete()
#         super(SingletonModel, self).save(*args, **kwargs)
#
#     @classmethod
#     def load(cls):
#         try:
#             return cls.objects.get()
#         except cls.DoesNotExist:
#             return cls()


class HomepageScopedSettings(ScopedSettings):
    pass


# FIXME: Bah, that ZipExtractorStorage can't work.
class ZipExtractorStorage(Storage):
    """Dummy"""

    def save(self, name, content, max_length=None):
        # with ZipFile(name) as zip_file:
        #     upload_path = self.get_upload_path(self, self.package.name)
        #     zip_file.extractall(self.get_upload_path() / self.slug)
        #     # TODO: do something with uploaded file
        pass


class Theme(models.Model):
    # TODO: determine a way to allow only own tenant's themes, or to explicitly allow others, per theme
    def get_upload_path(self, instance: "Theme", filename: str):
        return Path("themes")  # / instance.homepage.name

    slug = models.CharField(max_length=64, validators=[validate_slug])
    title = models.CharField(max_length=255)
    package = models.FileField(
        upload_to=get_upload_path, storage=ZipExtractorStorage, null=True, blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ColoredMixin(models.Model):
    class Meta:
        abstract = True

    color_accent = ColorField()
    text_primary = ColorField()
    text_secondary = ColorField()
    text_success = ColorField()
    text_danger = ColorField()
    text_warning = ColorField()
    text_info = ColorField()
    text_light = ColorField()
    text_dark = ColorField()
    text_muted = ColorField()
    text_white = ColorField()

    bg_primary = ColorField()
    bg_secondary = ColorField()
    bg_light = ColorField()
    bg_dark = ColorField()


class HomepageSite(TenantSite):
    subtitle = models.CharField(
        _("Subtitle"),
        help_text=_("Subtitle of the homepage"),
        max_length=255,
        blank=True,
    )
    logo_url = models.CharField(
        _("Logo URL"), help_text=_("Homepage Logo URL"), max_length=255, blank=True
    )
    # logo = models.ImageField()

    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class MultiHomepagesMixin(models.Model):
    """A mixin that can be added to a model to mark it as belonging to more than one homepage."""

    class Meta:
        abstract = True

    homepages = models.ManyToManyField(HomepageSite)


class SingleHomepageMixin(models.Model):
    class Meta:
        abstract = True

    homepage = models.ForeignKey(HomepageSite, on_delete=models.CASCADE)


# Note: SingleHomepageMixin is 2nd in the list, so that objects is called first from PolymorphicModel.
# This is needed for PolymorphicModel to get no ManagerInheritanceWarning.
class Block(PolymorphicModel, SingleHomepageMixin):
    """A basic HTML/renderable block.

    You can either create a Block directly, and fill out the title and content, and it will be rendered
    as HTML. The order of the block is determined by the "weight" property: the higher the weight, the
    "deeper" sinks the block down.

    If you subclass Block, you can add model fields. Just make sure you add these fields to the
    "additional_fields" list property, so they will be added to the template context.
    """

    class Meta:
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")

    additional_fields = []
    template_name = "block.html"

    title = models.CharField(_("Title"), max_length=50, blank=True)
    show_title = models.BooleanField(
        default=True, verbose_name=_("Show title on homepage")
    )
    content = models.TextField(_("Content"), blank=True)
    weight = models.SmallIntegerField(_("Weight"), default=0)

    # def __str__(self):
    # (
    #     f"{self.title} ({self.tenant.name})"
    #     if self.title
    #     else f"{self._meta.verbose_name.capitalize()} ({self.tenant.name})"
    # )

    def verbose_name(self):
        return self._meta.verbose_name

    def btype(self) -> str:
        """:returns the block type (=basically the lowercase class name) as string."""
        return self.__class__.__name__.lower()

    def __str__(self):
        return f"{self.title} ({self.homepage})"

    @property
    def tenant(self):
        return self.homepage.tenant


class Header(Block):
    class Meta:
        verbose_name = _("Header")
        verbose_name_plural = _("Headers")

    template_name = "header.html"
    additional_fields = ["logo", "background_image"]

    logo = models.ImageField(blank=True, null=True)
    background_image = models.ImageField(blank=True, null=True)


class News(Block):
    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

    template_name = "news.html"


class OpeningHours(Block):
    """Opening hours, that can be rendered in a block"""

    class Meta:
        verbose_name = _("Opening hours")
        verbose_name_plural = _("Opening hours")

    template_name = "opening_hours.html"
    additional_fields = ["entries", "weekdays_count"]

    def weekdays_count(self) -> int:
        """returns distinct count of week days that are open.

        E.g. if opening hours are MO 8-12, WE 8-12 + 15-18, FR 8-12; then it would return 3."""
        # FIXME: use a distinct call
        return self.entries.count()


class OpeningHourSlot(models.Model):
    """Single block of opening hours, e.g. '8:00 - 12:00'"""

    DAYS_CHOICES = (
        (0, _("MO")),
        (1, _("TU")),
        (2, _("WE")),
        (3, _("TH")),
        (4, _("FR")),
        (5, _("SA")),
        (6, _("SU")),
    )
    day = models.PositiveSmallIntegerField(
        choices=DAYS_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        null=True,
    )
    start = models.TimeField()
    end = models.TimeField()
    opening_hours = models.ForeignKey(
        OpeningHours, on_delete=models.CASCADE, related_name="entries"
    )

    def __str__(self) -> str:
        return f"{self.day_str()}, {self.start} - {self.end}"

    def is_today(self) -> bool:
        return datetime.today().weekday() == self.day

    def day_str(self) -> str:
        """returns the day as (translated) 2 char str."""
        return self.DAYS_CHOICES[self.day][1]


class Map(Block):
    """A Block with a GDPR-compliant map image pointing to a OSM, Google Maps, or other map service point."""

    class Meta:
        verbose_name = _("Map")
        verbose_name_plural = _("Maps")

    template_name = "map.html"
    additional_fields = ["address", "link_image", "location_url"]

    address = models.CharField(max_length=128, verbose_name=_("Address"))
    link_image = models.ImageField(upload_to="map_images", blank=True, null=True)
    location_url = models.URLField(
        max_length=255,
        verbose_name=_("Location URL"),
        help_text=_("Link to point in OSM, GMaps etc."),
    )


class Contact(Block):
    class Meta:
        verbose_name = _("Contact")

    def get_homepage_email(self):
        return self.tenant.email  # FIXME

    additional_fields = ["email"]
    template_name = "contact.html"

    email = models.EmailField()


class Team(Block):
    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    template_name = "team.html"
    additional_fields = ["members"]


class TeamMember(SingleHomepageMixin, models.Model):
    """A team member with a name, function, description and photo."""

    class Meta:
        verbose_name = _("Team member")
        verbose_name_plural = _("Team members")

    @staticmethod
    def _get_team():
        pass

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(_("Name"), max_length=50)
    function = models.CharField(_("Function"), max_length=50, blank=True)
    description = models.TextField(_("Description"), blank=True)
    image = models.ImageField(_("Photo"), blank=True, null=True)

    def __str__(self):
        return self.name

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        # FIXME: make homepage links work
        team, created = Team.objects.get_or_create(homepage=self.homepage)
        if created:
            team.tenant = self.homepage_set.foo

        self.team = team
        super().save(force_insert, force_update, using, update_fields)


class Qualification(models.Model):
    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")

    title = models.CharField(max_length=255)
    member = models.ForeignKey(
        TeamMember, on_delete=models.CASCADE, related_name="qualifications"
    )

    def __str__(self):
        return self.title


# def get_upload_path(instance: models.Model, filename: str):
#     model = instance.model.__class__._meta
#     name = model.tenant.id
#     return f"tenant_{name}/images/{filename}"


class Image(models.Model):
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    title = models.CharField(_("Title"), max_length=100, blank=True)
    image = models.ImageField(_("Image"), upload_to="images/")

    def __str__(self):
        return self.title if self.title else _("Image {}").format(self.id)


class Gallery(Block):
    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Galleries")

    images = models.ManyToManyField(Image)


class Footer(Block):
    class Meta:
        verbose_name = _("Footer")
        verbose_name_plural = _("Footers")

    template_name = "footer.html"
    additional_fields = ["vendor"]

    vendor = models.CharField(max_length=64, blank=True)
