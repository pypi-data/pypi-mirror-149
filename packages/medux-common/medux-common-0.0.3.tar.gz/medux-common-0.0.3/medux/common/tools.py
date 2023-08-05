from logging import getLogger
from typing import Dict, Union, List

from django.utils.translation import gettext_lazy as _
from django.db.models import Model  # FIXME could be a problem during migrations
from menu import MenuItem as SimpleMenuItem

logger = getLogger(__file__)


class MenuItem(SimpleMenuItem):
    """MedUX MenuItem with permission check.

    :param required_permission list|str: You can provide a list or a string as required permission for this
        menu item. If the user doesn't have that permission, the menu item will be invisible.
    :param classes: the CSS classes that will be added to the menu item
    :param badge str|callable: a callable that returns a str with the text of a badge, if needed.
    """

    def __init__(
        self,
        *args,
        required_permissions=None,
        classes=None,
        badge=None,
        **kwargs,
    ):
        if required_permissions is None:
            required_permissions = []
        elif not type(required_permissions) == list:
            required_permissions = [required_permissions]
        self.required_permissions = required_permissions
        # TODO add callable
        self.classes = classes
        self.badge = badge
        super().__init__(*args, **kwargs)

    def process(self, request):
        if callable(self.badge):
            self.badge = self.badge(request)
        super().process(request)


def create_groups_permissions(
    groups_permissions: Dict[str, Dict[Union[Model, str], List[str]]]
):
    """Creates groups and their permissions defined in given `groups_permissions` automatically.

    :param groups_permissions: a dict, see also `MeduxPluginAppConfig.groups_permissions`

    Based upon the work here: https://newbedev.com/programmatically-create-a-django-group-with-permissions

    """
    from django.apps import apps
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    for group_name in groups_permissions:

        # Get or create group
        # Translators: group name
        group, created = Group.objects.get_or_create(name=_(group_name))
        if created:
            group.save()

        # Loop models in group
        for model in groups_permissions[group_name]:
            # if model_class is written as dotted str, convert it to class
            if type(model) is str:
                model_class = apps.get_model(model)
            else:
                model_class = model

            # Loop permissions in group/model

            for perm_name in groups_permissions[group_name][model]:

                # Generate permission name as Django would generate it
                codename = f"{perm_name}_{model_class._meta.model_name}"

                try:
                    # Find permission object and add to group
                    content_type = ContentType.objects.get(
                        app_label=model_class._meta.app_label,
                        model=model_class._meta.model_name.lower(),
                    )
                    perm = Permission.objects.get(
                        content_type=content_type,
                        codename=codename,
                    )
                    group.permissions.add(perm)
                    logger.info(
                        f"  Adding permission '{codename}' to group '{group.name}'"
                    )
                except Permission.DoesNotExist:
                    logger.info(f"  ERROR: Permission '{codename}' not found.")
