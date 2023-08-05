from logging import getLogger

logger = getLogger(__name__)


class VirtualHostMiddleware:
    """A middleware that adds the current vhost, domain and subdomain as
     attributes to the request.

    The 'www' subdomain is ignored."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        vhost = request.get_host()
        request.vhost = vhost
        domain = vhost.split(":")[0]
        # ignored_prefix = "www."
        # if getattr(settings, "IGNORE_WWW_SUBDOMAIN", False) and domain.startswith(
        #     ignored_prefix
        # ):
        #     domain = domain.replace(ignored_prefix, "", 1)
        request.domain = domain
        domain_parts = domain.split(".")
        if len(domain_parts) > 2:
            # FIXME: only one level of subdomains supported...
            subdomain = domain_parts[0]
            if subdomain.lower() == "www":
                subdomain = None
        else:
            subdomain = None

        request.subdomain = subdomain

        logger.debug(f"Virtualhost: {request.domain}, Subdomain: {request.subdomain}")
        return self.get_response(request)
