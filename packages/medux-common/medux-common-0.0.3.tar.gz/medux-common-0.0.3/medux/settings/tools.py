from .registry import SettingsRegistry
from .models import ScopedSettings


def delete_orphaned_settings():
    """Finds orphaned keys and deletes them.

    At application start, MedUX creates settings from .toml files.
    However, Orphaned settings that are not used any more stay in the database and may produce poblems.
    This procedure deletes every setting that has no .toml setting equivalent.
    """
    orphaned_ids = []
    for item in ScopedSettings.objects.all():
        if not SettingsRegistry.exists(item.namespace, item.key, item.scope):
            # FIXME: take care of "orphaned" keys which are bound to a user,device, tenant.
            orphaned_ids.append(item.id)
    ScopedSettings.objects.filter(id__in=orphaned_ids).delete()
