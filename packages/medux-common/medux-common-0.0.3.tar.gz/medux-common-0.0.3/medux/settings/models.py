#  MedUX - Open Source Electronical Medical Record
#  Copyright (c) 2022  Christian González
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import Tuple, List

import enumfields
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from medux.common.models import Tenant, User
from medux.settings import KeyType, Scope
from medux.settings.registry import SettingsRegistry


class ScopedSettings(models.Model):

    """Convenience access model class for all scoped MedUX settings.

    You can easily access settings using ScopedSettings.get(namespace, key, scope, ...)
    """

    class Meta:
        verbose_name = verbose_name_plural = _("Scoped settings")
        ordering = ["namespace", "key", "scope"]
        unique_together = [
            # ["namespace", "key", "scope", "tenant"],
            ["namespace", "key", "scope", "group"],
            # ["namespace", "key", "scope", "device"],
            ["namespace", "key", "scope", "user"],
        ]
        permissions = [
            ("change_own_user_settings", _("Can change own user's scoped settings")),
            (
                "change_own_tenant_settings",
                _("Can change own tenant's scoped settings"),
            ),
            ("change_group_settings", _("Can change groups' scoped settings")),
        ]

    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    # device = models.ForeignKey(
    #     "Device", on_delete=models.CASCADE, default=None, null=True, blank=True
    # )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )
    namespace = models.CharField(max_length=25)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    scope = enumfields.EnumIntegerField(Scope)

    def clean(self):
        self.namespace = str(self.namespace).lower()
        self.key = str(self.key).lower()

    def field_name(self):
        """returns a combined name with namespace, key and scope."""
        return f"{self.namespace}__{self.key}__{self.scope.name.lower()}"

    @classmethod
    def create(cls, namespace: str, key: str, scope: Scope) -> None:
        """Creates an (empty) settings entry in the database.

        Does not overwrite existing values.
        """
        cls.assure_exists(namespace, key, scope)
        s, created = ScopedSettings.objects.get_or_create(
            namespace=namespace, key=key, scope=scope
        )
        if created:
            s.save()

    @classmethod
    def get(
        cls,
        namespace: str,
        key: str,
        scope: Scope,
        full_object: bool = False,
        user: User | None = None,
        group: Group | None = None,
        device=None,  # TODO add device support
        tenant: Tenant | None = None,
    ) -> int | str | bool | models.Model | None:
        """Retrieve a settings key in a convenient way.

        :returns: namespaced settings value, according to scope and, if applicable, the related
            object like user, group etc.
            If no object exists, return None.
            If pointing to an unregistered namespace/key, raise a KeyError.

        :param namespace: the namespace this key is saved under. Usually the app's name.
        :param key: the key to be retrieved
        :param scope: the scope that key is valid for. If scope is None, and more than one keys are
            saved under that scope, the key with the highest priority is taken:
            USER > DEVICE > GROUP > TENANT > VENDOR
        :param key_type: settings type: "str", "bool", "int"
        :param full_object: if True, return the complete model instance instead of only its value
        :param user: if scope is USER, you have to provide a User object
            that key/scope is valid for.
        :param group: if scope is GROUP, you have to provide a SettingsGroup object
            that key/scope is valid for.
        :param device: if scope is DEVICE, you have to provide a Device object
            that key/scope is valid for.
        :param tenant: if scope is TENANT, you have to provide a Tenant object
            that key/scope is valid for.

        """

        cls.assure_exists(namespace, key, scope)
        key_type = SettingsRegistry.key_type(namespace, key)

        filters = {
            "namespace": namespace,
            "key": key,
        }
        if scope:
            filters["scope"] = scope
            if scope == Scope.USER:
                filters["user"] = user
            elif scope == Scope.GROUP:
                filters["group"] = group
            elif scope == Scope.DEVICE:
                filters["device"] = device
            elif scope == Scope.TENANT:
                filters["tenant"] = tenant

        objects = ScopedSettings.objects.filter(**filters)
        if len(objects) == 0:
            # if this setting does not exist (yet), return None
            return None

        if len(objects) == 1:
            obj = objects.first()
            if full_object:
                return obj
            value = obj.value  # type: str
        else:
            # more than one scopes under that key and scope
            ids = ",".join(i.id for i in objects)
            raise KeyError(
                f"There are multiple settings keys under {namespace}.{key}[{scope}]: ids {ids}"
            )
        # filter out int and boolean values and return them instead.
        if key_type == KeyType.INTEGER:
            return int(value)
        if key_type == KeyType.BOOLEAN:
            if value.lower() == "false":
                return False
            elif value.lower() == "true":
                return True
            # maybe nullable/uninitialized boolean?
            elif value == "":
                return ""
            else:
                raise ValueError(f"DB value '{value}' cannot be casted into boolean!")
        if key_type == KeyType.STRING:
            return str(value)

        # should never happen...
        raise KeyError(f"Unknown settings type: {key_type}")

    @classmethod
    def set(
        cls,
        namespace: str,
        key: str,
        value: str | int | bool,
        scope: Scope,
        user=None,
        tenant=None,
        device=None,
        group: Group = None,
    ) -> None:

        """Sets a settings key."""

        cls.assure_exists(namespace, key, scope)
        # key_type is not used directly, as the value in the DB always is casted to a str.
        # Retrieving later is casted by the type saved in the SettingsRegistry.
        # key_type = SettingsRegistry.key_type(namespace, key)

        filter = {
            "namespace": namespace,
            "key": key,
            "scope": scope,
        }

        # set correct scope
        if scope == Scope.USER:
            if user is None:
                raise AttributeError(
                    "When scope==USER, a user object must be provided."
                )
            filter["user"] = user

        elif scope == Scope.DEVICE:
            if device is None:
                raise AttributeError(
                    "When scope==DEVICE, a device object must be provided."
                )
            filter["device"] = device

        elif scope == Scope.GROUP:
            if group is None:
                raise AttributeError(
                    "When scope==GROUP, a group object must be provided."
                )
            filter["group"] = group

        elif scope == Scope.TENANT:
            if tenant is None:
                raise AttributeError(
                    "When scope==TENANT, a tenant object must be provided."
                )
            filter["tenant"] = tenant

        # TODO: maybe do some casting / checks here?

        (item, created) = ScopedSettings.objects.get_or_create(**filter)
        item.value = str(value)
        item.save()

    @classmethod
    def keys(cls) -> List[Tuple[str, str]]:
        """:returns: a Tuple[namespace,key] of all currently available keys."""

        return [(item.namespace, item.key) for item in cls.objects.all()]

    @classmethod
    def namespaces(cls) -> list[str]:
        """:returns: a list of available namespaces."""
        # FIXME this is highly insufficient. distinct() would be better, but not available on SQLite/dev
        result = set()
        for s in ScopedSettings.objects.order_by("namespace").values_list(
            "namespace", flat=True
        ):
            result.add(s)
        return list(result)

    def __str__(self) -> str:
        # add user, tenant, group
        fk = ""
        if self.scope == Scope.USER:
            fk = f": '{self.user}'"
        elif self.scope == Scope.GROUP:
            fk = f": '{self.group}'"
        elif self.scope == Scope.TENANT:
            fk = f": '{self.tenant}'"
        a = f"{'.'.join([self.namespace, self.key])} [{self.scope.name}{fk}]: {self.value}"
        return a

    @classmethod
    def assure_exists(cls, namespace, key, scope) -> None:
        """Raises KeyError if given settings are not registered."""
        if not SettingsRegistry.exists(namespace, key, scope):
            raise KeyError(f"Setting {namespace}.{key}/{scope.name} is not registered.")
