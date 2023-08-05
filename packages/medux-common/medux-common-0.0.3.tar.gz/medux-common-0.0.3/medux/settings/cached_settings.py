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
from typing import Optional


class CachedSettings:
    """Creates a request specific set of settings, usable for templates.

    CachedSettings allows easy access to the settings for a specific context, given a request:

    CachedSettings(request).my_namespace.my_setting returns the specific setting. It respects the current
    user, groups, device, and tenant

    # It creates a dict with nested settings:
    # <namespace>
    # +-<key-1>
    #   +-user
    #   | +- value: 1
    #   | +- user: 23
    #   +-device
    #     +- value: 2
    #     +- device: 23543
    # ...
    """

    from django.http import HttpRequest

    class Namespace:
        """Transparently represents the first part (=namespace, before the dot) of a key, when
        accessed as CachedSettings' attribute, e.g.
        ```python
        settings = CachedSettings(request)
        settings.prescriptions.medication_message
        ```
        """

        from django.db.models import QuerySet
        from django.http import HttpRequest

        def __init__(self, request: HttpRequest, queryset: QuerySet, namespace: str):
            self.namespace = namespace
            self.queryset = queryset
            self.request = request

        def __repr__(self):
            return f"<Namespace '{self.namespace}'>"

        def __getattr__(self, key) -> str | None:
            """get a list of settings items with that key, ordered by scope:

            The scope order is: USER > DEVICE > GROUP > TENANT > VENDOR
            If a key is found during the traversal, its value is returned, else the next scope is
            looked up. If no key is found, None is returned.
            """
            from medux.settings.models import ScopedSettings
            from medux.settings import Scope

            value: Optional[str, int, bool] = ""
            for item in self.queryset.filter(key=key).order_by(
                "-scope"
            ):  # type: ScopedSettings
                scope = item.scope

                if scope == Scope.USER and self.request.user == item.user:
                    if not item.value:
                        continue
                    value = item.value
                    break

                # TODO: handle cookies/devices
                # if (
                #     current_scope == Scope.DEVICE
                #     and self.request.COOKIES["device"] == item.device
                # ):
                #     return item.value

                if scope == Scope.GROUP and item.group in self.request.user.groups:
                    if not item.value:
                        continue
                    value = item.value
                    break

                if scope == Scope.TENANT:
                    tenant = self.request.tenant
                    if tenant is None:
                        raise AttributeError(
                            "Could not determine tenant in current request. Aborting."
                        )
                    if tenant == item.tenant:

                        if not item.value:
                            continue
                        value = item.value
                        break
                    else:
                        # tenant of setting does not match current user's tenant
                        continue

                if scope == Scope.VENDOR:
                    value = item.value
                    break

            if value.isnumeric():
                value = int(value)
            elif value.lower() in ["true", "false"]:
                value = not value.lower() == "false"
            elif value == "":
                value = None
            return value

    def __init__(self, request: HttpRequest):
        from medux.settings.models import ScopedSettings

        self.request = request
        self.queryset = ScopedSettings.objects.select_related(None).all()
        # for item in self.queryset:
        # set scope /foreign objects as needed
        # if item.scope == Scope.USER:
        #     i["user"] = self.user
        # elif item.scope == Scope.GROUP:
        #     # FIXME: its groups, not group...! Enable more than 1 group!
        #     i["group"] = self.groups
        # elif item.scope == Scope.DEVICE:
        #     i["device"] = self.device

        # create namespace if necessary (dict)
        # if not self.all_settings.get(item.namespace):
        #     self.all_settings[item.namespace] = {}
        #
        # # create key if necessary (dict)
        # if not self.all_settings[item.namespace].get(item.key):
        #     self.all_settings[item.key] = {}
        #
        # self.all_settings[item.namespace][item.key][item.scope] = i

    def __getattr__(self, namespace):
        """Helper to retrieve settings key (all scopes) in a pythonic way:

        CachedSettings.<namespace>.<key>"""

        return self.Namespace(self.request, self.queryset, namespace)


# @receiver(request_finished)
# def on_request_finished(sender, **kwargs):
#     settings.invalidate()
