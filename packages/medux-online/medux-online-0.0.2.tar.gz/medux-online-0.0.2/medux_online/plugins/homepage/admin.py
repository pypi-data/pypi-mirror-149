from django.contrib import admin

from medux.common.models import Tenant
from medux_online.core.models import TermsAndConditionsPage, PrivacyPage
from medux_online.plugins.homepage.models import (
    TeamMember,
    Team,
    OpeningHours,
    Contact,
    Gallery,
    Footer,
    OpeningHourSlot,
    HomepageSite,
    Block,
    Qualification,
    Theme,
    Header,
    Map,
    Image,
)


class BlockAdmin(admin.ModelAdmin):
    model = Block
    list_filter = ["homepage"]
    list_display = ["title", "btype", "weight"]
    ordering = ["weight"]


class OpeningHourSlotInline(admin.TabularInline):
    extra = 5
    model = OpeningHourSlot


class OpeningHoursAdmin(admin.ModelAdmin):
    inlines = [OpeningHourSlotInline]


class QualificationInline(admin.TabularInline):
    model = Qualification
    extra = 3


class TeamMemberAdmin(admin.ModelAdmin):
    inlines = [QualificationInline]


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 3


class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]


class MapAdmin(admin.ModelAdmin):
    exclude = ("content",)


class StaticPageAdmin(admin.ModelAdmin):
    list_filter = ["site"]
    ordering = ["site", "version"]
    list_display = ["site", "version"]


class HomepageAdmin(admin.ModelAdmin):
    pass


admin.site.register(PrivacyPage, StaticPageAdmin)
admin.site.register(TermsAndConditionsPage, StaticPageAdmin)

admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(OpeningHours, OpeningHoursAdmin)
admin.site.register(Contact)
admin.site.register(Gallery)
admin.site.register(Image)
admin.site.register(Footer)
admin.site.register(Tenant)
admin.site.register(Block, BlockAdmin)
admin.site.register(Theme)
admin.site.register(Header)
admin.site.register(Map, MapAdmin)
admin.site.register(HomepageSite, HomepageAdmin)
# admin.site.register(OpeningHourSlot)

# don't show the original Django Site - it's replaced by Homepage
# admin.site.unregister(Site)
