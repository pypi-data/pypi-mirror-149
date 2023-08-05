from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django_hosts import patterns, host
from gdaps.pluginmanager import PluginManager

_pattern_list = []
for module in PluginManager.load_plugin_submodule("hosts"):
    if module.__name__.startswith("gdaps"):
        continue

    try:
        module_host_patterns = getattr(module, "host_patterns")
    except AttributeError:
        raise ImproperlyConfigured(
            f"'{module.__name__} does not define an 'host_pattern' attribute. "
        )
    _pattern_list += module_host_patterns

# application's main host patterns
host_patterns = patterns(
    "",
    host("", settings.ROOT_URLCONF, name="root"),
    *_pattern_list,
)
