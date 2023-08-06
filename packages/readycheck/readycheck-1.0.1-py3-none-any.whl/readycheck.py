"""Run custom checks on classes attributes when accessing them.

Does one thing, does it well.
"""

__title__ = "readycheck"
__author__ = "Loïc Simon"
__license__ = "MIT"
__copyright__ = "Copyright 2022 Loïc Simon"
__version__ = "1.0.1"
__all__ = ["ReadyCheck", "NotReadyError"]


from typing import Any, Callable, Iterator


class NotReadyError(RuntimeError):
    """An attribute is tried to be accessed before it is ready.

    Inherits from :exc:`RuntimeError`.

    Attributes:
        class_(type): The class holding the attribute to access.
        attr(str): The name of the attribute we tried to access.
    """
    def __init__(self, msg: str, class_: type, attr: str) -> None:
        super().__init__(msg)
        self.class_ = class_
        self.attr = attr


class _RCDict(dict):
    def __init__(
        self,
        _is_ready: Callable[[Any], bool] | None = None,
        _class: type | None = None,
        **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        if _is_ready is None:
            def _is_ready(item):
                return (item is not None)
        self._is_ready = _is_ready
        self._class = _class

    def __getitem__(self, name: str) -> Any:
        """Proxy item access"""
        val = self._get_raw(name)
        if self._is_ready(val):
            return val
        raise NotReadyError(f"'{name}' is not ready yet!", self._class, name)

    def _get_raw(self, name: str) -> Any:
        """Raw item access"""
        try:
            val = super().__getitem__(name)
        except KeyError:
            if self._class:
                raise AttributeError(
                    f"'{self._class.__qualname__}' has no attribute '{name}'"
                ) from None
            else:
                raise AttributeError(f"No attribute '{name}'") from None
        return val


class _RCMeta(type):
    def __new__(
        metacls,
        name: str,
        bases: tuple[type],
        dict: dict[str, Any],
        check: Callable[[Any], bool] | None = None,
        check_type: type | None = None,
    ) -> type:
        # register directly private/magic names only
        _prv_dict = {name: dict[name] for name in dict if name.startswith("_")}
        return super().__new__(metacls, name, bases, _prv_dict)

    def __init__(
        cls,
        name: str,
        bases: tuple[type],
        dic: dict[str, Any],
        check: Callable[[Any], bool] | None = None,
        check_type: type | None = None,
    ) -> None:
        _prv_dict = {name: dic[name] for name in dic if name.startswith("_")}
        _pub_dict = {name: dic[name] for name in dic if name not in _prv_dict}
        super().__init__(name, bases, _prv_dict)
        _is_ready = check
        if check_type:
            if check:
                def _is_ready(item):
                    return isinstance(item, check_type) and check(item)
            else:
                def _is_ready(item):
                    return isinstance(item, check_type)
        cls._rc_dict = _RCDict(_is_ready=_is_ready, _class=cls, **_pub_dict)

    def __getattr__(cls, name: str) -> Any:
        if name.startswith("_"):
            # Private/magic name: dont search in ._rc_dict (infinite recursion)
            raise AttributeError(f"'{cls.__name__}' has no attribute '{name}'")
        return cls._rc_dict[name]

    def __setattr__(cls, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            cls._rc_dict[name] = value

    def __delattr__(cls, name: str) -> None:
        if name.startswith("_"):
            super().__delattr__(name)
        else:
            del cls._rc_dict[name]

    def __iter__(cls) -> Iterator:
        return iter(cls._rc_dict)

    def get_raw(cls, attr: str) -> Any:
        return cls._rc_dict._get_raw(attr)


class ReadyCheck(metaclass=_RCMeta):
    """Proxy class to prevent accessing not initialized objects.

    When accessing a class attribute, this class:
        - returns its value (classic behavior) if it is evaluated
          *ready* (see below);
        - raises a :exc:`NotReadyError` exception otherwise.

    Subclass this class to implement *readiness* check on class attributes
    and define *readiness* as needed. By default, attributes are
    considered *not ready* only if their value is ``None``::

        class NotNone(ReadyCheck):
            a = None            # NotNone.a will raise a NotReadyError
            b = <any object>    # NotNone.b will be the given object

    Use ``check_type`` class-definition argument to define readiness based
    on attributes types (using :func:`isinstance()`)::

        class MustBeList(ReadyCheck, check_type=list):
            a = "TBD"           # MustBeList.a will raise a NotReadyError
            b = [1, 2, 3]       # MustBeList.b will be the given list

    Use ``check`` class-definition argument to define custom readiness
    check (``value -> bool`` function)::

        class MustBePositive(ReadyCheck, check=lambda val: val > 0):
            a = 0               # MustBePositive.a will raise a NotReadyError
            b = 37              # MustBePositive.b will be 37

    If both arguments are provided, attribute type will be checked first
    and custom check will be called only for suitable attributes.

    Attributes can be set, updated and deleted the normal way.
    *Readiness* is evaluated at access time, so changing an attribute's
    value will change its readiness with no additional work required, and
    attributes set after class definition also benefit the checking proxy.

    Note:
        Attributes whose name start with ``"_"`` (private and magic attributes)
        are not affected and will be returned even if *not ready*.

    These classes also implement the iterating protocol to provide access
    to protected attributes **names** (order preserved)::

        for name in NotNone:
            print(name)         # Will print "a" then "b"

    Warning:
        Classes deriving from this class are not meant to be instantiated.
        Due to the checking proxy on class attributes, instances will not
        see attributes defined at class level, and attributes defined in
        ``__init__`` or after construction will **not** be ready-checked.

        This class relies on a custom metaclass: you will not be able to
        create mixin classes from this one and a custom-metaclass one.

    .. py:classmethod:: get_raw(name)

        Access to an attribute bypassing ready check.

        :param str name: name of the attribute. This must be a
            **public** attribute (no leading underscore).
        :returns: The attribute value, whatever it is.
        :raises AttributeError: if the attribute dosent exist.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError(
            "ReadyCheck-derived classes are not meant to be instantiated!"
        )

    # Everything is in the metaclass!
