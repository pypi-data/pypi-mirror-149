from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from medux.common.models import TenantSite, TenantMixin
from medux_online.plugins.homepage.models import Theme


class CreatedUpdatedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# www.sozialversicherung.at/HELP/VSNR/VSNR_1.htm
def validate_svnr(value: str):
    if len(value) != 10:
        raise ValidationError(_("SVNR must have 10 digits."))
    if not value.isnumeric():
        raise ValidationError(_("SVNR must only contain digits."))

    if value[0] == "0":
        raise ValidationError(_("SVNR cannot start with '0'."))

    weights = (3, 7, 9, None, 5, 8, 4, 2, 1, 6)
    sum = 0
    for index, c in enumerate(value):
        # multiple digits by specific "weight"
        if weights[index]:
            sum += int(c) * weights[index]

    # Prüfziffer = Gewichtete Summe MOD 11
    mod = sum % 11
    if int(value[3]) != mod:
        raise ValidationError(_("SVNR not valid."))

    if int(value[4:6]) > 31:  # day
        raise ValidationError(_("Day of birth date can not be higher than 31."))


class PrescriptionRequest(CreatedUpdatedMixin, TenantMixin, models.Model):
    class Meta:
        permissions = [
            ("approve_prescription_request", _("Can approve prescription requests"))
        ]
        verbose_name = _("Prescription request")
        verbose_name_plural = _("Prescription requests")

    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    last_name = models.CharField(verbose_name=_("Last name"), max_length=100)
    first_name = models.CharField(verbose_name=_("First name"), max_length=100)
    insurance_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), validate_svnr],
        verbose_name=_("Insurance number"),
    )
    comment = models.TextField(
        blank=True,
        help_text=_("Please enter your medication requests here."),
    )
    internal_comment = models.CharField(
        blank=True, verbose_name=_("Internal Comment"), max_length=300
    )
    approved = models.BooleanField(default=False, verbose_name=_("Approved"))

    def __str__(self):
        return f"{self.last_name.upper()},{self.first_name}, {self.insurance_number}"

    def priority(self):
        """returns a (configurable) priority for this instance.

        This is used for ordering.
        :return: a str with an integer from 1 - 5, which represents
            low - high priority
        """
        # TODO: make it configureable via settings: (1,2,5
        timediff = timezone.now() - self.created
        if timediff.total_seconds() < 1 * 60 * 60:  # <1 hour
            return 1
        elif timediff.total_seconds() < 2 * 60 * 60:  # <2 hours
            return 2
        elif timediff.total_seconds() < 5 * 60 * 60:  # <5 hours
            return 3
        elif timediff.total_seconds() < 24 * 60 * 60:  # <24 hours
            return 4
        # > 24 hrs
        return 5


class Medication(models.Model):
    name = models.CharField(_("Medication"), max_length=255)
    pkgs = models.PositiveSmallIntegerField(default=1)
    signature = models.CharField(max_length=100)
    request = models.ForeignKey(PrescriptionRequest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, OP {self.pkgs}, S: {self.signature}"


class PrescriptionsSite(TenantSite):
    """A prescriptions site that allows patients to get medication
    etc."""

    # TODO: maybe reduce dependency on homepage module here?
    @property
    def theme(self):
        """Either returns the homepage's theme, or, if not applicable,
        the default one."""
        if hasattr(self.tenantedsite_ptr, "homepage"):
            return self.tenantedsite_ptr.homepage.theme
        else:
            return Theme.objects.get(pk=1)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """Always sets tenant to the homepage's tenant"""
        self.tenant = self.tenant
        self.domain = self.domain.lower()
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _("Prescriptions Site")
        verbose_name_plural = _("Prescriptions Sites")
