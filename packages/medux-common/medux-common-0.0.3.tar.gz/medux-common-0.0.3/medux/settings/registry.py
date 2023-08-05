import logging

from .definitions import Scope, KeyType

logger = logging.getLogger(__file__)


class SettingsRegistry:
    """A in-memory storage where settings namespaces/keys/scopes are registered at
    application start and can be checked against for existence and type.

    Every available setting *must* be registered before usage.
    """

    _registered_keys: list[tuple[str, str, Scope]] = []
    _key_types: dict[tuple[str, str], KeyType] = {}

    def __init__(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} is not meant to be instantiated."
        )

    @classmethod
    def register(
        cls,
        namespace,
        key,
        allowed_scopes: list["Scope"] = None,
        key_type=KeyType.STRING,
    ):
        """Registers a settings variable in a global list.

        This makes sure that settings variables read in from e.g. .toml files can only be accepted if they
        match existing, already registered settings.
        :param namespace: The namespace of the key
        :param key: the key name
        :param allowed_scopes: a list of allowed `Scope`s. VENDOR will be added automatically.
        :param key_type: the type of the setting. Other types are not allowed at assignment later.
        """

        # VENDOR scope is always allowed
        if allowed_scopes is None:
            allowed_scopes = []
        if Scope.VENDOR not in allowed_scopes:
            allowed_scopes.append(Scope.VENDOR)

        for scope in allowed_scopes:
            t = (namespace, key, scope)
            # can't register same key again...
            if t in cls._registered_keys:
                logger.warning(
                    f"Key {namespace}.{key} [{scope.name}] was already registered!"
                )
            else:
                cls._registered_keys.append(t)
                cls._key_types[(namespace, key)] = key_type

    @classmethod
    def exists(cls, namespace, key, scope) -> bool:
        """:returns: True if there was a setting with given namespace.key/scope registered."""

        # return (namespace, key, scope) in cls._registered_keys
        return (namespace, key, scope) in cls._registered_keys

    @classmethod
    def scopes(cls, namespace: str, key: str) -> set:
        """:returns: a set of scopes registered under the given namespaced settings key."""
        scopes = set()
        for s in cls._registered_keys:
            if s[0] == namespace and s[1] == key:
                scopes.add(s[2])
        return scopes

    @classmethod
    def key_type(cls, namespace: str, key: str) -> KeyType:
        """:returns: the type of the given namespaced settings key."""
        t = (namespace, key)
        if t in cls._key_types:
            return cls._key_types[t]
        else:
            raise KeyError(f"No setting '{namespace}.{key}' registered.")

    @classmethod
    def all_dct(cls) -> dict[str, dict[str, str]]:
        _all = {}
        for namespace, key, scope in cls._registered_keys:
            if namespace not in _all:
                _all[namespace] = {}
            if key not in _all[namespace]:
                _all[namespace][key] = {}

            _all[namespace][key][scope] = ""
        return _all

    @classmethod
    def all(cls) -> tuple[str, str, str, str]:
        """:returns: a tuple of all registered settings keys: namespace, key, scope, key_type"""
        for setting_tuple in cls._registered_keys:
            yield setting_tuple + (cls._key_types[setting_tuple[0:2]],)
