from django.utils.translation import gettext_lazy as _

from . import __version__
from .api import MeduxPluginAppConfig


class CommonPluginMeta:
    """This configuration is the introspection data for plugins."""

    # the plugin machine "name" is taken from the AppConfig, so no name here
    verbose_name = _("Common")
    author = "Christian González"
    author_email = "christian.gonzalez@nerdocs.at"
    vendor = "Nerdocs"
    description = _(
        "MedUX common tools and models, which are used for medux_online and medux"
    )
    category = _("Base")
    visible = True
    version = __version__
    # compatibility = "medux.core>=2.3.0"


class CommonConfig(MeduxPluginAppConfig):
    """A GDAPS Django app plugin.

    It needs a special parameter named ``PluginMeta``. It is the key for GDAPS
    to recognize this app as a GDAPS plugin.
    ``PluginMeta`` must point to a class that implements certain attributes
    and methods.
    """

    name = "medux.common"
    default = True  # FIXME: Remove when django bug is fixed

    # This is the most important attribute of a GDAPS plugin app.
    PluginMeta = CommonPluginMeta

    def initialize(self):
        pass
