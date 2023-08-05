from logging import getLogger
from typing import List, Dict

from django.apps import AppConfig
from django.utils.functional import cached_property

logger = getLogger(__file__)


class MeduxPluginAppConfig(AppConfig):
    """Common base class for all MedUX AppConfigs.

    All MedUX apps' AppConfigs must inherit from this class (or must at least implement this interface).
    """

    from django.db import models

    # A dict that defines groups and their permissions this Plugin provides.
    #   You can call :class:`medux.common.tools.create_groups_permissions()`
    #   when the application is initialized.
    #   Example:
    #   groups_permissions = {
    #       'Group name': {
    #           SomeModel_or_dotted_model_path: ['add', 'change', 'delete', 'view'],
    #           ...
    #       }
    #   }
    #   Note: the "Group name" is translatable, just set the English name here.
    #   You can use a model class or a dotted model path like "auth.user"
    groups_permissions: Dict[str, Dict[models.Model, List[str]]] = {}

    def initialize(self):
        """Initializes the application at setup time.

        This method is called from the "initialize" management command.
        It should set up basic data in the database etc., and needs to be idempotent.
        """

    @cached_property
    def compatibility_errors(self) -> List[str]:
        """checks for compatibility issues that can't be ignored for correct application function,
         and returns a list of errors.

        :returns a list of error strs"""

        return []

    @cached_property
    def compatibility_warnings(self) -> List[str]:
        """Checks for compatibility issues that can be accepted for continuing.

        :returns: a list of warnings"""

        return []
