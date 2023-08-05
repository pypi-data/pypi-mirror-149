from django_hosts import host

from .models import TenantSite


def host_patterns_factory(tenanted_site: type(TenantSite), root_url: str):
    host_patterns = []
    for site in tenanted_site.objects.all():
        host_patterns.append(
            host(
                regex=site.domain + r".*$",
                urlconf=root_url,
                # FIXME use proper name/slug here:
                name=f"{site.__class__.__name__.lower()}_{site.slug}",
            )
        )
    return host_patterns
